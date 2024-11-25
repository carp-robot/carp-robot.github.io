import cv2

# Video filenames
video_files = [
    "BID_droptoy_static.mov",
    "BID_droptoy_stochastic.mov",
    "vanilla_droptoy_statifc.mov",
    "vanilla_droptoy_stochastic.mov"
]

# Function to get video duration
def get_video_duration(video_file):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Failed to open video file: {video_file}")
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    return duration

# Get the duration of each video
durations = {}
for video in video_files:
    duration = get_video_duration(video)
    if duration is not None:
        durations[video] = duration

# Find the longest video duration
longest_video = max(durations, key=durations.get)
longest_duration = durations[longest_video]

# Function to extend video by last frame to match the target duration
def extend_video(video_file, target_duration):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Failed to open video file: {video_file}")
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"extended_{video_file}", fourcc, fps, (frame_width, frame_height))
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    last_frame = None

    for _ in range(frame_count):
        ret, frame = cap.read()
        if ret:
            last_frame = frame
            out.write(frame)

    current_duration = frame_count / fps
    extra_frames = int((target_duration - current_duration) * fps)

    for _ in range(extra_frames):
        out.write(last_frame)

    cap.release()
    out.release()

# Extend all videos to match the longest duration
for video in video_files:
    if video != longest_video:
        extend_video(video, longest_duration)

print(f"Longest video: {longest_video} with duration: {longest_duration} seconds")
