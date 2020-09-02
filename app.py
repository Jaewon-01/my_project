from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.



## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
  #  rank_receive = request.form['rank_give']
    food_type_receive = request.form['food_type_give']
    title_receive = request.form['title_give']
    review_receive = request.form['review_give']
    rate_receive = request.form['rate_give']
    address_receive = request.form['address_give']
    distance_receive = request.form['distance_give']



    # DB에 삽입할 review 만들기
    review = {
     #   'rank': rank_receive,
        'food_type': food_type_receive,
        'title': title_receive,
        'review': review_receive,
        'rate': rate_receive,
        'address': address_receive,
        'distance': distance_receive
    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})




@app.route('/review/delete', methods=['POST'])
def delete_review():
    # title_receive로 클라이언트가 준 title 가져오기
    title_receive = request.form['title_give']
    db.reviews.delete_one({'title': title_receive})
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 삭제되었습니다.'})


@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})









if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)