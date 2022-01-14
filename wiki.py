# -*- coding: utf-8 -*-
import wikipedia as wiki
import argparse


def print_list_of_content_blocks(content_dict: dict):
    '''
    pass
    '''
    content_dict_keys = list(content_dict.keys())
    if len(content_dict_keys) == 0:
        print("Статья пустая")
    else:
        print("Содержание статьи: \n")
        for i, header in enumerate(content_dict_keys):
            print(f"{i+1} -- {header}")


def get_content_blocks_dict(article: str):
    '''
    pass
    '''
    article_split = article.split("== ")
    content_dict = {}
    content_dict["Аннотация"] = article_split[0]
    for content in article_split[1:]:
        content_split = content.split(" ==")
        title_of_content_block = content_split[0]
        content_dict[title_of_content_block] = content_split[1]
    return content_dict

    

def get_content_of_article(name: str) -> str:
    '''
    Возвращает полный текст статьи 
    
    Параметры: 
            name (str): название статьи
    '''
    try:
        return wiki.page(name).content
    except Exception:
        print("Такой статьи не существует")        
    
    
def get_summary_of_article(name: str) -> str:
    '''
    Возвращает аннотацию статьи
    
    Параметры:
            name (str): название статьи
    '''
    try:
        return wiki.summary(name)
    except Exception:
        print("Такой статьи не существует")
    

def get_list_of_results(request: str, max_results_number: int) -> list:
    '''
    Возвращает список результатов по текстовому запросу
    
    Параметры:
            request (str)            : текстовый запрос на поиск в Википедии
            max_results_number (int) : максимальное число результатов поиска
            
    Возвращает:
            result_of_search (list): список с реультатами поиска
    '''
    result_of_search = wiki.search(request, results=max_results_number)
    if len(result_of_search) == 0:
        print(f"Результаты по запросу {request} не найдены. Повторите попытку")
    else:
        print("Результаты поиска: ")
        for i, result in enumerate(result_of_search):
            print(f"{i+1} -- {result}")
        return result_of_search
    

def set_language(language: str):
    '''
    Устанавливает язык, на котором будут выдаваться статьи
    
    Параметры:
            language (str): язык
    '''
    if language in wiki.languages():
        wiki.set_lang(language)
    else:
        raise Exception(f"{language} doesn't exists")
        

def parse_args():
    '''
    Парсер аргументов
    '''
    parser = argparse.ArgumentParser(
            description="Утилита для получения статей из Википедии"
    )
    parser.add_argument(
            "-r", "--request", type=str, help="Запрос на поиск в Википедии"
    )
    parser.add_argument(
            "-n", "--number", type=int, help="Максимальное число результатов поиска"
    )
    parser.add_argument(
            "-l", "--language", type=str, help="Язык, на котором будут выводиться статьи"
    )
    arguments = parser.parse_args()
    return arguments
    

def main():
    '''
    Точка входа в скрипт
    '''
    arguments = parse_args()
    
    request            = arguments.request
    language           = arguments.language
    max_results_number = arguments.number 
    
    set_language(language)
    #results = get_list_of_results(request, max_results_number)
    
    while True:
        results = get_list_of_results(request, max_results_number)
        number_of_article = int(input("\nВведите номер интересующей Вас статьи: "))
        if number_of_article == 0 or number_of_article > len(results) + 1:
            print(f"Статьи с номером {number_of_article} нет в результатах поиска. Повторите попытку")
            continue
        else:
            name_of_article = results[number_of_article - 1]
            
            summary_or_full = input("\nХотите вывести аннотацию (summary), содержание (content) или полный текст статьи (full)? (S/C/F): ")
            summary_or_full = summary_or_full.lower()
            if summary_or_full == "s":
                summary = get_summary_of_article(name_of_article)
                print("\n")
                print(summary)
                
            elif summary_or_full == "c":
                content = get_content_of_article(name_of_article)
                content_dict = get_content_blocks_dict(content)
                content_dict_keys = list(content_dict.keys())
                
                while True:
                    print_list_of_content_blocks(content_dict)
                    number_of_block = int(input("\nВведите номер интересующего блока статьи: "))
                    if number_of_block == 0 or number_of_block > len(content_dict_keys) + 1:
                        print(f"Блока с номером {number_of_block} нет для данной статьи. Повторите попытку")
                        continue
                    else:
                        print("\n")
                        print(content_dict[content_dict_keys[number_of_block - 1]].strip("="))
                        
                        stay_on_this_artcile = input("Хотите остаться на этой статье или перейти к следующей? (Y/N): ")
                        choice = stay_on_this_artcile.lower()
                        
                        if choice == "y":
                            continue
                        elif choice == "n":
                            break
                        else:
                             raise Exception("f{choice} doesn't exist in [Y, N]")
                        
            elif summary_or_full == "f":
                content = get_content_of_article(name_of_article)
                print("\n")
                print(content)
            
            continue_or_not = input("\nХотите продолжить? (Y/N) : ")
            continue_or_not = continue_or_not.lower()
            if continue_or_not == "y":
                continue
            elif continue_or_not == "n":
                print("\nЗавершаю работу...")
                break
            else:
                raise Exception("f{continue_or_not} doesn't exist in [Y, N]")
        
        
if __name__ == "__main__":
    main()
        
    
    
    
        
        
        
    
    
    
    
            
        
    

        
    
    