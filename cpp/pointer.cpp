uint16_t** frames[2];

frames[0] = (uint16_t**) malloc(MAX_FRAME_COUNT * sizeof(uint16_t**));
frames[1] = (uint16_t**) malloc(MAX_FRAME_COUNT * sizeof(uint16_t**));

for(){
frames[0][frameCount] = (uint16_t*) malloc(FRAME_WIDTH * FRAME_HEIGHT * sizeof(uint16_t));
CHECK_MALLOC(frames[0][frameCount]);
frames[1][frameCount] = (uint16_t*) malloc(FRAME_WIDTH * FRAME_HEIGHT * sizeof(uint16_t));
CHECK_MALLOC(frames[1][frameCount]);
}

for(){
free(frames[0][frameId]);
free(frames[1][frameId]);
}

free(frames[0]);
free(frames[1]);
