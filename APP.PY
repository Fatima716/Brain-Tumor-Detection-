from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# تحميل النموذج المحفوظ
model = load_model('brain_tumor_classifier.h5')

# تجميع النموذج (إذا لم يكن مجمعًا)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# وظيفة لتحضير الصورة للتنبؤ
def prepare_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

# وظيفة للتنبؤ بالصورة
def predict_image(model, img_path):
    img_array = prepare_image(img_path)
    prediction = model.predict(img_array)
    return 'تحتوي على ورم في الدماغ' if prediction[0][0] > 0.5 else 'لا تحتوي على ورم في الدماغ'

# الصفحة الرئيسية لتحميل الصورة
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
[            file.save(filepath)
            result = predict_image(model, filepath)
            return render_template('result.html', result=result, img_path=filepath)
    return render_template('index.html')

# إعدادات لتشغيل التطبيق
if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

ig['UPLOAD_FOLDER'])
    app.run(debug=True)