# Personal-Ai-Trainer

Staying at home for long periods of time can become boring, especially when most fun activities are done outdoors. Still, this is not an excuse to be unproductive and the extra available time is an excellent opportunity to work on your own health. Typical gyms come with a variety of equipment and trainers who can tell you what to do. The lack of these in one's home can often be the culprit that stops them from working out. It would be great if there existed a personal trainer that could help you ace your workouts at home. What if it could also count the repetitions of each exercise so that you can put all your concentration and energy to do one more push up?

This AI can help you ace your workout sessions at home without the need for fitness trainers by detecting, tracking and analyzing your body movements and giving appropriate instructions just as a fitness coach would do.

Python, opencv and mediapipe framework was used in bulding this model

## Usage

1. Install MediaPipe following the instructions on the [MediaPipe website](https://mediapipe.readthedocs.io/en/latest/install.html).

2. Clone this repository and navigate to the `volume_control` directory.

3. Run the pipeline using the following command:
```bash
mediapipe run --calculator_graph_config_file=volume_control.pbtxt --input_stream=input_video:<path_to_input_video> --output_stream=output_video:<path_to_output_video>
