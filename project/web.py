import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, Response

from build_heatmap import create_heatmaps
from ll import find_by_column
from plot import build_plot, build_plot2, build_plot3, build_plot4
from plot2 import sum_revenue_for_org_in_period, sum_revenue_for_industry_in_period, universal_search, sum_column
from utils import parse_file, sum_by_period

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('download_page.html')

@app.route("/general")
def general():
    print("CAUGHT - GENERAL")
    return render_template("general_page.html")


@app.route("/upload", methods=['POST'])
def upload():
    print("file was uploaded")
    file = request.files['file']
    parse_file(file)
    print(file.filename)
    return jsonify({'message': f'Файл принят'})


@app.route("/search", methods=['POST'])
def search():
    data = request.json
    print(data.get("fromDate"))
    return {}


@app.route("/search_all", methods=['POST'])
def search_all():
    data = request.json
    salary = sum_by_period("выручка", "ДОРАДО ФИРМА ИЧП ФОМИНА", "2016", "2019")
    print(salary)
    return {}


@app.route("/graphics", methods=['POST'])
def graphics():
    file = pd.read_csv("industrial_registry.csv")
    start_year = int(request.json.get("periodFrom"))
    end_year = int(request.json.get("periodTo"))
    print(start_year, end_year)
    build_plot(file, start_year, end_year)
    return jsonify(success=True)

@app.route("/graphics2", methods=['POST'])
def graphics2():
    file = pd.read_csv("industrial_registry.csv")
    start_year = int(request.json.get("periodFrom"))
    end_year = int(request.json.get("periodTo"))
    industry = request.json.get("industry")
    print(industry)
    print(start_year, end_year)
    build_plot2(industry, start_year, end_year, industry)
    return jsonify(success=True)

@app.route("/graphics3", methods=['POST'])
def graphics3():
    file = pd.read_csv("industrial_registry.csv")
    start_year = int(request.json.get("periodFrom"))
    end_year = int(request.json.get("periodTo"))
    industry = request.json.get("industry")
    print(industry)
    print(start_year, end_year)
    build_plot3(industry, start_year, end_year)
    return jsonify(success=True)

@app.route("/graphics4", methods=['POST'])
def graphics4():
    build_plot4()
    return jsonify(success=True)


@app.route("/get_revenue", methods=['POST'])
def get_revenue():
    data = request.get_json()
    specialization = data.get('specialization')
    print(specialization)
    start_year = int(data.get('periodFrom'))
    end_year = int(data.get('periodTo'))

    value = data.get('value')
    if specialization == "организация":
        return jsonify({"sum": str(sum_revenue_for_org_in_period(pd.read_csv("industrial_registry.csv"), value,start_year, end_year)),
                        "sum2": str(universal_search(pd.read_csv("industrial_registry.csv"), value, start_year, end_year, "Наименование организации",
                                                     "прибыль")),
                        "sum3": str(universal_search(pd.read_csv("industrial_registry.csv"), value, start_year, end_year, "Наименование организации",
                                                     "персонала")),
                        })
    elif specialization == "индустрия":
        return jsonify({"sum": str(sum_revenue_for_industry_in_period(pd.read_csv("industrial_registry.csv"), value, start_year, end_year)),
                        "sum2": str(universal_search(pd.read_csv("industrial_registry.csv"), value,start_year, end_year,
                                                     "Основная отрасль",
                                                     "прибыль")),
                        "sum3":str(universal_search(pd.read_csv("industrial_registry.csv"), value,start_year, end_year,
                                                     "Основная отрасль",
                                                     "персонала")),
                        })
    elif specialization == "общее":
        return jsonify({"sum": str(
           sum_column("выручка")),
                        "sum2": str(sum_column("прибыль")),
                        "sum3": str(sum_column("персонала"))
                        })
    return {}
@app.route("/industry")
def industry():
    return render_template("industry_page.html")


@app.route("/all-industries", methods=['POST'])
def get_all_industries():
    all_industries = list(set(find_by_column("Основная отрасль").to_list()))
    return jsonify({"industries": all_industries})


@app.route("/all-orgs", methods=['POST'])
def get_all_orgs():
    all_industries = list(set(find_by_column("Наименование организации").to_list()))
    return jsonify({"org": all_industries})


@app.route("/org")
def organization():
    return render_template("organization_page.html")

@app.route("/heatmap", methods=['POST'])
def heatmap():
    create_heatmaps(pd.read_csv("industrial_registry.csv"))







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




