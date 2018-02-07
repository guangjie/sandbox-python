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

    fuzzy_car_brand = input_car_brand()

    db_connection = get_database_connection(config)

    possible_car_brands = get_possible_car_brands_from_db(db_connection, fuzzy_car_brand)

    exact_car_brand_id = get_exact_car_brand_id(possible_car_brands)

    fuzzy_comma_separated_car_countries = input_car_countries()

    possible_countries = get_possible_car_countries_from_db(db_connection, fuzzy_comma_separated_car_countries)

    exact_car_countries = get_exact_car_country_ids(possible_countries)

    output_sql = prepare_output_sql(exact_car_brand_id, exact_car_countries)

    fuzzy_car_parent_ident_code = input_car_parent_model()

    possible_car_parent_ident_code = get_possible_car_parent_ident_code_from_db(db_connection, fuzzy_car_parent_ident_code, exact_car_brand_id)

    exact_car_parent_ident_code = get_exact_car_parent_model(possible_car_parent_ident_code)

    parent_model = get_parent_model_from_db(db_connection, exact_car_parent_ident_code)

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

            if ans_confirm_parent_model['confirm_parent'] is True:
                parent_model_sql = prepare_parent_model_sql(parent_model)

        else:
            print('nothing found')

    sql_models = prepare_full_model_sql()

    output_sql += sql_models
    print(output_sql)

    prepare_sql_file(output_sql)


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


def get_possible_car_parent_ident_code_from_db(connection, fuzzy_parent_model_name, brand_id):
    cursor = connection.cursor()

    sql = "SELECT `ident_code`, `name`"
    sql += "FROM `mdx_kfz`.`mdx_kfz_models` "
    sql += "WHERE `name` LIKE '%{}%' ".format(fuzzy_parent_model_name)
    sql += "AND `herst` = {};".format(brand_id)

    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def get_parent_model_from_db(connection, parent_ident_code):
    print(parent_ident_code)
    cursor = connection.cursor()

    sql = "SELECT `id` "
    sql += "FROM `mdx_kfz`.`mdx_kfz_models` "
    sql += "WHERE `ident_code` = '{}';".format(parent_ident_code)

    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def get_exact_car_brand_id(possible_car_brands):
    question_to_ask = 'Which is the Brand of Car?'
    return get_exact_answers(possible_car_brands, question_to_ask)


def get_exact_car_country_ids(possible_countries):
    question_to_ask = 'Select countries which will have these models?'
    return get_exact_answers(possible_countries, question_to_ask, 'multiple')


def get_exact_car_parent_model(possible_car_parent_models):
    question_to_ask = 'Which is the ident_code for the Parent?'
    return get_exact_answers(possible_car_parent_models, question_to_ask)


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
    question = "What is the Brand of Car?"
    return input_single_text_question(question)


def input_car_countries():
    question = "Which countries would you like to add? Comma separate for multiple values."
    return input_single_text_question(question)


def input_car_parent_model():
    question = "What is the Indent Code of the parent model? Leave empty if none."
    return input_single_text_question(question)


def input_new_car_models():
    question = "List the new models separated with comma."
    return question


def input_new_ident_codes():
    question = "List the new model ident_code separated with comma."
    return question


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


def prepare_output_sql(car_brand_id, exact_car_countries):
    output_sql = "SET @HertzId = {}; \n".format(car_brand_id)
    country_sql = ''

    for selected_country in exact_car_countries:
        output_sql += "SET @CountryId{} = {};\n".format(selected_country['selection'], selected_country['value'])
        country_sql += prepare_country_sql(selected_country['selection'])

    output_sql += country_sql
    return output_sql


def prepare_country_sql(country_name):
    stripped_country_name = country_name.replace(' ', '')

    output_sql = "INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) \n"
    output_sql += "SELECT * FROM (SELECT @ModelId, @CountryId{}) AS tmp \n".format(stripped_country_name)
    output_sql += "WHERE NOT EXISTS ( \n"
    output_sql += "\t SELECT `id` FROM `mdx_kfz_model_countries` \n"
    output_sql += "\t WHERE `id` = @ModelId AND `countryId` = @CountryId{} \n".format(stripped_country_name)
    output_sql += ") LIMIT 1; \n\n"

    return output_sql


def prepare_parent_model_sql(parent_model):
    output_sql = "SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = '{}'); \n\n".format(parent_model)
    output_sql += "INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) \n"
    output_sql += "SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp \n"
    output_sql += "WHERE NOT EXISTS ( \n"
    output_sql += "\t" + "SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent \n"
    output_sql += ") LIMIT 1; \n\n"

    return output_sql


def prepare_model_sql(ident_code, car_model):
    output_sql = "SET @IdentCode = '{}'; \n".format(ident_code)
    output_sql += "SET @ModelName = '{}'; \n\n".format(car_model)

    output_sql += "INSERT INTO `mdx_kfz_models` (`herst`, `name`, `ident_code`) \n"
    output_sql += "SELECT * FROM (SELECT @HertzId, @ModelName, @IdentCode) AS tmp \n"
    output_sql += "WHERE NOT EXISTS ( \n"
    output_sql += "\t SELECT `ident_code` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode \n"
    output_sql += ") LIMIT 1; \n\n"

    output_sql += "SET @ModelId = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode); \n\n"

    return output_sql


def prepare_full_model_sql():
    new_car_model_names = input_new_car_models()
    new_car_ident_codes = input_new_ident_codes()

    output_sql = ''

    dict_models = new_car_model_names.split(',')
    dict_ident_codes = new_car_ident_codes.split(',')

    for idx_car_model, car_model in enumerate(dict_models):
        str_ident_code = str(dict_ident_codes[idx_car_model])
        str_car_model = str(car_model)

        output_sql += prepare_model_sql(str_ident_code, str_car_model)

    return output_sql


def prepare_sql_file(output_sql):
    with open('../outputs/new_models.sql', 'w') as fout:
        fout.write(output_sql)


if __name__ == '__main__':
    main()