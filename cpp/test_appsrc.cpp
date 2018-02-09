#include "rtsp_rkencoder.h"


using namespace std;

typedef struct
{
  guint8 level;
  GstClockTime timestamp;
} MyContext;

pthread_mutex_t Image2_mutex = PTHREAD_MUTEX_INITIALIZER;//互斥锁

unsigned char _image1[640*480*3];//双缓冲
unsigned char _image2[640*480*3];//直接给推流用

int _image_width=640;
int _image_height=480;
#define FPS 	15

/* called when we need to give data to appsrc 
给图像数据
*/
static void
need_data (GstElement * appsrc, guint unused, MyContext * ctx)
{
  GstBuffer *buffer;
  guint size;
  GstFlowReturn ret;

  size = _image_width * _image_height * 3;//width*height*3,RGB24

  buffer = gst_buffer_new_allocate(NULL, size, NULL);//gstreamer/gst/gstbuffer.c
  /* this makes the image black/white */
  //gst_buffer_memset (buffer, 0, ctx->white ? 0xff : 0x0, size);////gstreamer/gst/gstbuffer.c
  
  /*现在想办法把自己的图像给进去*/
  pthread_mutex_lock (&Image2_mutex);
  //gst_buffer_fill (buffer,0, &_image2[0],size);
  //ctx->white = !ctx->white;
  gst_buffer_memset (buffer, 0, ctx->level, size);
  pthread_mutex_unlock (&Image2_mutex);
  ctx->level += 4;
  /* increment the timestamp every 1/2 second */
  GST_BUFFER_PTS (buffer) = ctx->timestamp;
  GST_BUFFER_DURATION (buffer) = gst_util_uint64_scale_int (1, GST_SECOND, FPS);
  ctx->timestamp += GST_BUFFER_DURATION (buffer);

  g_signal_emit_by_name (appsrc, "push-buffer", buffer, &ret);
  gst_buffer_unref(buffer); // dkorobkov: add to prevent memory leak
}

/* called when a new media pipeline is constructed. We can query the
 * pipeline and configure our appsrc */
static void
media_configure (GstRTSPMediaFactory * factory, GstRTSPMedia * media,
    gpointer user_data)
{
  GstElement *element, *appsrc;
  MyContext *ctx;

  /* get the element used for providing the streams of the media */
  element = gst_rtsp_media_get_element (media);

  /* get our appsrc, we named it 'mysrc' with the name property */
  appsrc = gst_bin_get_by_name_recurse_up (GST_BIN (element), "mysrc");

  /* this instructs appsrc that we will be dealing with timed buffer */
  gst_util_set_object_arg (G_OBJECT (appsrc), "format", "time");
  /* configure the caps of the video */
  g_object_set (G_OBJECT (appsrc), "caps",
      gst_caps_new_simple ("video/x-raw",
          "format", G_TYPE_STRING, "RGB",//"RGB16"应该指的是一共16位,"RGB"-->RGB24
          "width", G_TYPE_INT, _image_width,
          "height", G_TYPE_INT, _image_height,
          "framerate", GST_TYPE_FRACTION, 1, FPS, NULL), NULL);

  ctx = g_new0 (MyContext, 1);
  ctx->level = 0;
  ctx->timestamp = 0;
  /* make sure ther datais freed when the media is gone */
  g_object_set_data_full (G_OBJECT (media), "my-extra-data", ctx,
      (GDestroyNotify) g_free);

  /* install the callback that will be called when a buffer is needed */
  g_signal_connect (appsrc, "need-data", (GCallback) need_data, ctx);
  gst_object_unref (appsrc);
  gst_object_unref (element);
}

void * _run(void *id)
{
  GMainLoop *loop;
  GstRTSPServer *server;
  GstRTSPMountPoints *mounts;
  GstRTSPMediaFactory *factory;
  gst_init (NULL, NULL);

  loop = g_main_loop_new (NULL, FALSE);

  /* create a server instance */
  server = gst_rtsp_server_new ();
  //gst_rtsp_server_set_address(server,"192.168.168.191");//本地作为服务器地址，不用修改ip
  gst_rtsp_server_set_service(server,"6668");//修改port
  //gst_rtsp_server_set_service(server,m_str_port.c_str());//修改port
  /* get the mount points for this server, every server has a default object
   * that be used to map uri mount points to media factories */
  mounts = gst_rtsp_server_get_mount_points (server);

  /* make a media factory for a test stream. The default media factory can use
   * gst-launch syntax to create pipelines.
   * any launch line works as long as it contains elements named pay%d. Each
   * element with pay%d names will be a stream */
  factory = gst_rtsp_media_factory_new ();
  /*gst_rtsp_media_factory_set_launch (factory,
      "( appsrc name=mysrc ! videoconvert ! mpph264enc ! rtph264pay name=pay0 pt=96 )");//格式转换没有报错，mpph264enc还没测试
*/
  gst_rtsp_media_factory_set_launch (factory,
      "( appsrc name=mysrc caps=video/x-raw,format=(string)RGB,width=(int)640,height=(int)480,framerate=(fraction)15/1 ! videoconvert ! capsfilter caps=video/x-raw,format=(string)NV12 ! queue ! mpph264enc ! rtph264pay name=pay0 pt=96 )");//格式转换没有报错，mpph264enc还没测试

  /*gst_rtsp_media_factory_set_launch (factory,
      "( appsrc name=mysrc ! videoconvert ! capsfilter caps=video/x-raw,format=(string)NV12,width=(int)640,height=(int)480,framerate=(fraction)15/1 ! mpph264enc ! rtph264pay name=pay0 pt=96 )");//格式转换没有报错，mpph264enc还没测试
*/
  /* notify when our media is ready, This is called whenever someone asks for
   * the media and a new pipeline with our appsrc is created */
  g_signal_connect (factory, "media-configure", (GCallback) media_configure,
      NULL);

  /* attach the test factory to the /test url */
  gst_rtsp_mount_points_add_factory (mounts, "/test", factory);

  /* don't need the ref to the mounts anymore */
  g_object_unref (mounts);

  /* attach the server to the default maincontext */
  gst_rtsp_server_attach (server, NULL);

  /* start serving */
  g_print ("stream ready at rtsp://local(xxx.xxx.xxx.xxx):6668/test\n");
  g_main_loop_run (loop);
}

rtsp_264::rtsp_264()//初始化
{
  m_str_port = "6668";
  for(long i=0;i<640*480*3;i++)
    _image2[i]=0xff;//white
}

void rtsp_264::run()
{
  pthread_t threads;
  int id=0;
  pthread_create(&threads, NULL, _run, (void *)id);
}

void rtsp_264::refresh(unsigned char *image)//更新推流的帧
{
  if(image)
  {
    for(long i=0;i<640*480*3;i++)
    _image1[i]=image[i];//先复制到image1
    g_print ("refresh done\n");
  }
  else{
    for(long i=0;i<640*480*3;i++)
    _image1[i]=0xff;//先复制到image1
  }
  pthread_mutex_lock (&Image2_mutex);
  
  cout << "before refresh,image2 first 1 data:"<< _image2[0]<<endl;
  for(long i=0;i<640*480*3;i++)
    _image2[i]=_image1[i];//然后复制到image2
  cout << "after refresh,image2 first 1 data:"<< _image2[0]<<endl;
  pthread_mutex_unlock (&Image2_mutex);
    g_print ("refresh to image2 done\n");
}
  
