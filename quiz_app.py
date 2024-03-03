import streamlit as st
import xml.etree.ElementTree as ET

def load_quiz_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    quiz_data = []
    for question in root.findall('question'):
        question_text = question.find('text').text
        choices = [choice.text for choice in question.find('choices')]
        answer = int(question.find('answer').text)  # 答えは0-indexedにする
        quiz_data.append({'question': question_text, 'choices': choices, 'answer': answer})
    return quiz_data

def main():
    st.title('クイズアプリ')
    st.write('このアプリは、XMLファイルからクイズデータを読み込みます。')

    quiz_file = st.file_uploader('クイズデータ（XMLファイル）をアップロードしてください。', type=['xml'])
    if quiz_file is not None:
        quiz_data = load_quiz_data(quiz_file)

        total_questions = len(quiz_data)
        correct_answers = 0

        result_flag = st.button('結果判定', key='結果判定')
        
        for i, quiz in enumerate(quiz_data):
            st.subheader(f'Question {i+1}/{total_questions}')
            st.write(quiz['question'])
            selected_option = st.radio('選択肢', quiz['choices'], index=None)   # 初期状態では何も選択しない
            if result_flag:
                if quiz['choices'][quiz['answer']] == selected_option:
                    st.write('正解！🎉')
                    correct_answers += 1
                else:
                    st.write('不正解…😔')

        st.write(f'正解数: {correct_answers}/{total_questions}')
        accuracy = correct_answers / total_questions * 100 if total_questions > 0 else 0
        st.write(f'正解率: {accuracy:.2f}%')

if __name__ == '__main__':
    main()
