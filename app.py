import io

from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *

from flask import Flask, request, Response

app = Flask(__name__)

# 提取通用代码
# choices:  CPU, GPU0...GPU7
#device.set(device=DeviceId.GPU0)
device.set(device=DeviceId.CPU)
plt.style.use('dark_background')
colorizer = get_image_colorizer(artistic=True)
torch.backends.cudnn.benchmark = True


@app.route('/action', methods=['POST', 'GET'])
def action():
    file = request.files['file']
    img_name = file.filename
    _, ext = os.path.splitext(img_name)
    img_in_memory = io.BytesIO(file.read())

	#此处的35应该是种子而不是参数 可以改成25或者什么的，影响似乎不大
    img_ret = colorizer.get_transformed_image(img_in_memory, 35, watermarked=False)
    # colorizer.plot_transformed_image(path='C:/Users/PiaoZhenJia/Pictures/微信图片_20230728194252.png',
    #                                  render_factor=35, results_dir=Path('D:/'), post_process=False, watermarked=False)

    img_ret_bytes = io.BytesIO()
    img_ret.save(img_ret_bytes, format='PNG')
    img_ret_bytes.seek(0)
    res = Response(img_ret_bytes)
    res.headers.add('Content-Type', 'image/' + ext)
    res.headers.add('Content-Disposition', f'attachment; filename=colorize_{img_name}')
    return res

def main():
    app.run(port=5000, host="0.0.0.0", debug=False)


if __name__ == '__main__':
    main()

