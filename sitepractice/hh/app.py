from flask import Flask, request, render_template
from parser import fetch_resume_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query', '')
        area = request.form.get('area', 1)
        page_size = request.form.get('page_size', 20)
        exp_period = request.form.get('exp_period', 'all_time')
        logic = request.form.get('logic', 'normal')
        order_by = request.form.get('order_by', 'relevance')

        resumes = fetch_resume_data(query=query, area=area, page_size=page_size,
                                    exp_period=exp_period, logic=logic, order_by=order_by)

        return render_template('results.html', resumes=resumes)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
