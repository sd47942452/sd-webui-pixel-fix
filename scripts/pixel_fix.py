from PIL import Image
import gradio as gr
import modules.scripts as scripts
from modules import images
from modules.shared import opts


class Script(scripts.Script):
    print('像素修复插件已加载...')

    def title(self):
        return "像素修复"

    # 显示插件界面
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    # 加载UI
    def ui(self, is_img2img):
        with gr.Accordion("像素修复", open=False):
            with gr.Row():
                enabled = gr.Checkbox(label="Enable(是否启用)", value=False)

            with gr.Column():
                with gr.Row():
                    pixel_size = gr.Slider(label="Pixel Size recommend：8(像素颗粒大小，推荐值：8)", minimum=1, maximum=32,
                                           step=1, value=8)

        return [enabled, pixel_size]

    # 读取图片进程
    def postprocess(self, p, processed, enabled, pixel_size):

        # 是否启用
        if not enabled:
            return

        # 简单的像素对齐处理
        def process_image(original_image):
            small = original_image.resize((original_image.width // pixel_size, original_image.height // pixel_size),
                                          resample=Image.NEAREST)
            return small.resize((original_image.width, original_image.height), resample=Image.NEAREST)

        # 批量处理
        for i in range(len(processed.images)):
            pixel_image = process_image(processed.images[i])
            processed.images.append(pixel_image)
            images.save_image(pixel_image, p.outpath_samples, "pixel",
                              processed.seed + i, processed.prompt, opts.samples_format, info=processed.info, p=p)

        return processed
