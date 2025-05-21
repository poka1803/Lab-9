from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(basedir, 'instance', 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HardwarePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<HardwarePart {self.device} - {self.price}>'

if not os.path.exists(os.path.join(basedir, 'instance')):
    os.makedirs(os.path.join(basedir, 'instance'))
    print(f"Создана папка instance по пути: {os.path.join(basedir, 'instance')}")

try:
    with open(db_path, 'a'):
        pass
    print(f"Файл базы данных доступен для записи по пути: {db_path}")
except IOError as e:
    print(f"Ошибка доступа к файлу базы данных: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        device = request.form['device']
        price = float(request.form['price'])
        
        new_part = HardwarePart(device=device, price=price)
        db.session.add(new_part)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    parts = HardwarePart.query.all()
    total = sum(part.price for part in parts)
    
    return render_template('index.html', parts=parts, total=total)

@app.route('/delete/<int:id>')
def delete(id):
    part = HardwarePart.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных и таблицы успешно созданы")
    
    print(f"Приложение запущено. База данных находится по пути: {db_path}")
    app.run(debug=True)