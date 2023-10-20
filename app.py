from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS 扩展
import pymysql

app = Flask(__name__)
CORS(app)  # 在Flask应用上启用CORS

# 之后是您现有的代码...


app = Flask(__name__)

# 连接到MySQL数据库
db = pymysql.connect(
   host='localhost',  # 数据库主机地址
   user='root',       # 数据库用户名
   password='111111',   # 数据库密码
   database='shujuku'    # 数据库名称
)

@app.route('/addCalculation', methods=['POST'])
def add_calculation():
    try:
        # 获取前端发送的数据
        data = request.get_json()
        content = data.get('content', '')
        result = data.get('result', '')

        # 插入数据到数据库
        cursor = db.cursor()
        sql = "INSERT INTO calculations (content, result) VALUES (%s, %s)"
        cursor.execute(sql, (content, result))
        db.commit()

        # 查询插入后的自增ID
        cursor.execute("SELECT LAST_INSERT_ID()")
        calculation_id = cursor.fetchone()[0]
        cursor.close()

        return jsonify({'success': True, 'id': calculation_id})
    except Exception as e:
        return jsonify({'success': False, 'message': '计算插入失败', 'error': str(e)})

@app.route('/getCalculations', methods=['GET'])
def get_calculations():
    try:
        cursor = db.cursor()
        # 查询所有计算记录
        sql = "SELECT id, content, result FROM calculations"
        cursor.execute(sql)
        records = cursor.fetchall()
        calculations = [{'id': record[0], 'content': record[1], 'result': record[2]} for record in records]
        cursor.close()
        return jsonify({'success': True, 'calculations': calculations})
    except Exception as e:
        return jsonify({'success': False, 'message': '获取计算记录失败', 'error': str(e)})




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
