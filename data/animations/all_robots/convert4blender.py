import json
import numpy as np

def convert_to_anim(in_file, out_file):
# in_file = '133_pcl-1000-100_ex_0_animation_NO_PLAN.txt'
# out_file = "133_pcl-1000-100_ex_0_animation_NO_PLAN_converted.txt"
    with open(in_file) as json_file:
        data = json.load(json_file)
        num_segments = 1    # always 1 for pushing ??
        output_str = f"animation: [ <{num_segments}>\n"
        segment_id = 1
        start_segment_frame = 0
        frame_names = ["floor", "box", "finger", "target"]
        num_frames = len(frame_names)
        z_threshold_finger = 0.61
        # if there will be more than 1 segment, then we should loop over num_segment as well
        for d in data:
            print(d)
            if d == 'start':
                output_str += f"{d}: [ <{segment_id}> {start_segment_frame}]\n"
            elif d == 'frameIDs':
                f_ids = np.arange(num_frames)
                f_ids_str = "{0}".format(' '.join(map(str, f_ids)))
                output_str += f"{d}: [ <{num_frames}> {f_ids_str}]\n"
            elif d == 'frameNames':
                f_n_str = "{0}".format(' '.join(map(str, frame_names)))
                output_str += f"{d}: [ <{num_frames}> {f_n_str}]\n"
            # added the 4th color/transparency param for the 'floor' on the saved json file
            elif d == 'frameColors':
                output_str += f"{d}: [ <{num_frames} 4>\n"
                for c in data[d]:
                    if len(c) == 3:
                        c.append(1.0)
                        # print(c)
                    f_color = "{0}".format(' '.join(map(str, c)))
                    output_str += f"{f_color}\n"
                output_str += "]\n"
            elif d == 'poses':
                i = 0
                num_pose = len(data[d])
                output_str += f"{d}: [ <{num_pose} {num_frames} 7>\n"
                for pose in data[d]:
                    i += 1
                    j = 0
                    for f_p in pose:
                        j += 1
                        if (j % 3) == 0:
                            f_p[2] = max(z_threshold_finger, f_p[2])
                            # print("j: ", j, "\t", f_p)

                        f_pose = "{0}".format(' '.join(map(str, f_p)))
                        output_str += f"{f_pose}\n"
                        # print(f"{f_p}")

                    if i == num_pose:
                        print("i: ", i)
                        output_str += "]\n"
                        break

                    output_str += "\n"  # print empty line btw pose list for each timestep
            elif d == 'plan':
                num_plan_steps = len(data[d])
                # n x 6 (3D: finger + box)
                output_str += f"{d}: [ <{num_plan_steps} 6>\n"
                for plan_step in data[d]:
                    finger_box_pos = "{0}".format(' '.join(map(str, plan_step)))
                    output_str += f"{finger_box_pos}\n"
                output_str += "]"

        output_str += "]"   # close the animation
        # print(output_str)
        file_anim = open(out_file, 'w')
        file_anim.write(output_str)
