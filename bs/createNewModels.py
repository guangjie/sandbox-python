import json
import inquirer
import pymysql

def main():
    with open('../config.json') as json_data_file:
        config = json.load(json_data_file)

    if is_set(config, 'createNewModels'):
        settings = config['createNewModels']
    else:
        start_config(config)

    output_sql = ''

    app_question = [
        inquirer.Text(
            'car_brand',
            message="What is the Brand of Car?"
        )
    ]

    app_answer = inquirer.prompt(app_question)

    while app_answer['car_brand'] == '':
        app_answer = inquirer.prompt(app_question)

    conn_params = config['mysql']

    conn = pymysql.connect(
        host=conn_params['host'],
        user=conn_params['user'],
        password=conn_params['password'],
        # db=conn_params['db'],
        port=conn_params['port']
    )

    cursor = conn.cursor()
    sql = 'SELECT `id`, `name` FROM `mdx_kfz`.`mdx_kfz_herst` ' \
          'WHERE `name` ' \
          'LIKE "%' + app_answer["car_brand"] + '%";'

    cursor.execute(sql)
    result = cursor.fetchall()

    # print(result)

    brand_choices = []
    brand_dict = {}

    for row in result:
        brand_choices.append(row[1])
        brand_dict[row[1]] = row[0]

    app_question = [inquirer.List(
        'car_brand',
        message="Which is the Brand of Car?",
        choices=brand_choices
    )]

    app_answer = inquirer.prompt(app_question)

    output_sql += 'SET @HertzId = ' + str(brand_dict[app_answer['car_brand']]) + ';' + "\n"

    app_question = [inquirer.Text(
        'car_countries',
        message="Which countries would you like to add? Comma seperated for multiple values."
    )]

    app_answer = inquirer.prompt(app_question)

    countries_ans = app_answer["car_countries"].replace(',', '|')
    if countries_ans == '':
        countries_ans = 'China'

    sql = "SELECT `id`, `name` " \
          "FROM `mdxcnt`.`mdx_countries` " \
          "WHERE `name` REGEXP '" + countries_ans + "' OR `iso` REGEXP '" + countries_ans + "' OR `iso3` REGEXP '" + countries_ans + "';"
    cursor.execute(sql)
    possible_countries = cursor.fetchall()

    country_choices = []
    country_dict = {}

    for possible_country in possible_countries:
        country_choices.append(possible_country[1])
        country_dict[possible_country[1]] = possible_country[0]

    app_question = [inquirer.Checkbox(
        'car_countries',
        message="Which countries will have these models?",
        choices=country_choices
    )]

    app_answer = inquirer.prompt(app_question)

    country_sql = ''

    for selected_country in app_answer["car_countries"]:
        output_sql += 'SET @CountryId' + str(selected_country) + ' = ' + str(country_dict[selected_country]) + ";\n"
        country_sql += 'INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) ' + "\n" \
                       'SELECT * FROM (SELECT @ModelId, @CountryId' + str(selected_country).replace(' ', '') + ') AS tmp ' + "\n" \
                       'WHERE NOT EXISTS (' + "\n" \
                            "\t" + 'SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryId' + str(selected_country).replace(' ', '') + "\n"\
                       ') LIMIT 1;' + "\n\n"

    # print(output_sql)
    # print(country_sql)

    question_parent_model = [inquirer.Text(
        'car_parent_model',
        message="What is the Indent Code of the parent model? Leave empty if none."
    )]

    answer_parent_model = inquirer.prompt(question_parent_model)

    sql = "SELECT `id` " \
          "FROM `mdx_kfz`.`mdx_kfz_models` " \
          "WHERE `ident_code` = '" + answer_parent_model['car_parent_model'] + "';"
    cursor.execute(sql)
    parent_model = cursor.fetchall()

    ans_confirm_parent_model = {}
    ans_confirm_parent_model['confirm_parent'] = False

    while ans_confirm_parent_model['confirm_parent'] is False:
        if parent_model:
            qn_confirm_parent_model = [
                inquirer.Confirm(
                    'confirm_parent',
                    message="Parent model found: " + str(parent_model[0][0]) + ". Proceed?",
                    default='Y'
                )
            ]

            ans_confirm_parent_model = inquirer.prompt(qn_confirm_parent_model)
            # print(ans_confirm_parent_model)

            parent_model_sql = ''

            if ans_confirm_parent_model['confirm_parent'] is True:
                parent_model_sql = "SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = '" + answer_parent_model['car_parent_model'] + "');" + "\n\n"
                parent_model_sql += "INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) \n"
                parent_model_sql += "SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp \n"
                parent_model_sql += "WHERE NOT EXISTS ( \n"
                parent_model_sql += "\t" + "SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent \n"
                parent_model_sql += ") LIMIT 1; \n\n"
                # print(parent_model_sql)

        else:
            print('nothing found')

    qn_new_models = [
        inquirer.Text(
            'car_models_name',
            message="List the new models separated with comma"
        ),
        inquirer.Text(
            'car_ident_code',
            message="List the new model ident_code separated with comma"
        )
    ]

    ans_new_models = {}
    ans_new_models['car_models_name'] = ''
    ans_new_models['car_ident_code'] = ''

    while ans_new_models['car_models_name'] == '' or ans_new_models['car_ident_code'] == '':
        ans_new_models = inquirer.prompt(qn_new_models)

    dict_models = ans_new_models['car_models_name'].split(',')
    dict_ident_codes = ans_new_models['car_ident_code'].split(',')
    sql_models = ''

    for idx_car_model, car_model in enumerate(dict_models):
        sql_models += "SET @IdentCode = '" + str(dict_ident_codes[idx_car_model]) + "'; \n"
        sql_models += "SET @ModelName = '" + str(car_model) + "'; \n\n"

        sql_models += "INSERT INTO `mdx_kfz_models` (`herst`, `name`, `ident_code`) \n"
        sql_models += "SELECT * FROM (SELECT @HertzId, @ModelName, @IdentCode) AS tmp \n"
        sql_models += "WHERE NOT EXISTS ( \n"
        sql_models += "\t SELECT `ident_code` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode \n"
        sql_models += ") LIMIT 1; \n\n"

        sql_models += "SET @ModelId = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode); \n\n"
        sql_models += country_sql
        sql_models += parent_model_sql

    output_sql += sql_models
    print(output_sql)

    with open('../outputs/new_models.sql', 'w') as fout:
        fout.write(output_sql)

def is_set(dictionary, key):
    if dictionary.get(key):
        return True
    return False


def start_config(config):
    config_questions = [
        inquirer.Text(
            'database',
            message="What is the Database Name?"
        ),
        inquirer.Text(
            'table_brand',
            message="What is the Vehicle Brand Tablename?"
        ),
        inquirer.Text(
            'table_model',
            message="What is the Vehicle Model Tablename?"
        ),
        inquirer.Text(
            'table_model_countries',
            message="What is the Vehicle Model Countries Tablename?"
        ),
        inquirer.Text(
            'table_model_parent',
            message="What is the Vehicle Model Parent Tablename?"
        ),
        inquirer.Text(
            'table_model_i18n',
            message="What is the Vehicle Model Localization Tablename?"
        )
    ]

    config_answers = inquirer.prompt(config_questions)
    config['createNewModels'] = config_answers

    with open('config.json', 'w') as fout:
        # saves config dict into file
        json.dump(config, fout)


if __name__ == '__main__':
    main()