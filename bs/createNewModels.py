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

    car_brand = input_car_brand()

    db_connection = get_database_connection(config)

    possible_car_brands = get_possible_car_brands_from_db(db_connection, car_brand)

    exact_car_brand_id = get_exact_car_brand_id(possible_car_brands)

    output_sql += 'SET @HertzId = ' + exact_car_brand_id + ';' + "\n"

    comma_separated_car_countries = input_car_countries()

    possible_countries = get_possible_car_countries_from_db(db_connection, comma_separated_car_countries)

    exact_car_countries = get_exact_car_country_ids(possible_countries)

    country_sql = ''

    for selected_country in exact_car_countries:
        output_sql += 'SET @CountryId' + selected_country['selection'] + ' = ' + selected_country['value'] + ";\n"
        country_sql += 'INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) ' + "\n" \
                       'SELECT * FROM (SELECT @ModelId, @CountryId' + selected_country['selection'].replace(' ', '') + ') AS tmp ' + "\n" \
                       'WHERE NOT EXISTS (' + "\n" \
                            "\t" + 'SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryId' + selected_country['selection'].replace(' ', '') + "\n"\
                       ') LIMIT 1;' + "\n\n"

    print(output_sql)
    print(country_sql)

    question_parent_model = [inquirer.Text(
        'car_parent_model',
        message="What is the Indent Code of the parent model? Leave empty if none."
    )]

    answer_parent_model = inquirer.prompt(question_parent_model)

    cursor = db_connection.cursor()

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

            parent_model_sql = ''

            if ans_confirm_parent_model['confirm_parent'] is True:
                parent_model_sql = "SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = '" + answer_parent_model['car_parent_model'] + "');" + "\n\n"
                parent_model_sql += "INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) \n"
                parent_model_sql += "SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp \n"
                parent_model_sql += "WHERE NOT EXISTS ( \n"
                parent_model_sql += "\t" + "SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent \n"
                parent_model_sql += ") LIMIT 1; \n\n"

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

    with open('../config.json', 'w') as fout:
        # saves config dict into file
        json.dump(config, fout)


def get_database_connection(config):
    conn_params = config['mysql']

    connection = pymysql.connect(
        host=conn_params['host'],
        user=conn_params['user'],
        password=conn_params['password'],
        # db=conn_params['db'],
        port=conn_params['port']
    )

    return connection


def get_possible_car_brands_from_db(connection, fuzzy_brand_name):
    cursor = connection.cursor()

    sql = "SELECT `id`, `name` FROM `mdx_kfz`.`mdx_kfz_herst` " \
          "WHERE `name` " \
          "LIKE '%" + fuzzy_brand_name + "%';"

    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def get_possible_car_countries_from_db(connection, fuzzy_country_names='China'):
    cursor = connection.cursor()

    fuzzy_country_names = fuzzy_country_names.replace(',', '|')

    sql = "SELECT `id`, `name` " \
          "FROM `mdxcnt`.`mdx_countries` " \
          "WHERE `name` REGEXP '" + fuzzy_country_names + "' " \
             "OR `iso` REGEXP '" + fuzzy_country_names + "' " \
             "OR `iso3` REGEXP '" + fuzzy_country_names + "';"

    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def get_exact_car_brand_id(possible_car_brands):
    question_to_ask = 'Which is the Brand of Car?'
    return get_exact_answers(possible_car_brands, question_to_ask)


def get_exact_car_country_ids(possible_countries):
    question_to_ask = 'Select countries which will have these models?'
    return get_exact_answers(possible_countries, question_to_ask, 'multiple')


def get_exact_answers(possible_answers, qn, qn_type='single', required=True):
    tmp_choices = []
    tmp_dict = {}

    for answer in possible_answers:
        tmp_choices.append(answer[1])
        tmp_dict[answer[1]] = answer[0]

    if qn_type is not 'single':
        question = [inquirer.Checkbox(
            'tmp_answer',
            message=qn,
            choices=tmp_choices
        )]
    else:
        question = [inquirer.List(
            'tmp_answer',
            message=qn,
            choices=tmp_choices
        )]

    answer = inquirer.prompt(question)

    if required:
        while not answer:
            answer = inquirer.prompt(question)

    ans_list = []

    if qn_type is not 'single':
        for choice in answer['tmp_answer']:
            item_dict = {'selection': str(choice), 'value': str(tmp_dict[choice])}
            ans_list.append(item_dict)
        return ans_list

    return str(tmp_dict[answer['tmp_answer']])


def input_car_brand():
    question = 'What is the Brand of Car?'
    return input_single_text_question(question)


def input_car_countries():
    question = 'Which countries would you like to add? Comma separate for multiple values.'
    return input_single_text_question(question)


def input_single_text_question(question, required=True):
    question = [
        inquirer.Text(
            'temp_answer',
            message=question
        )
    ]

    answer = inquirer.prompt(question)

    if required:
        while not answer:
            answer = inquirer.prompt(question)

    return answer['temp_answer']


if __name__ == '__main__':
    main()