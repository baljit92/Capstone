import sys
import io

word_dict = {}

word_embedding_file = "word_embeddings/wiki-news-300d-1M-subword.vec"
word_subset_file = "word_embeddings/vector_subset.txt"
train_path = "raw_text.txt"
label_path = "label_mapping.txt"


def generate_mapping():
    label_list = []

    with open(train_path, 'r', encoding='utf-8') as infile:
        for oneline in infile.readlines():
            onelabel = oneline.strip().split('|||')[0].strip()

            if onelabel not in label_list:
                label_list.append(onelabel)

    
    label_dict = {}
    with open(label_path, 'w') as outfile1:
        for index in range(len(label_list)):
            print(str(label_list[index]) + ": " + str(index))
            
            label_dict[label_list[index]] = index

            oneline = str(label_list[index]) + " ||| " + str(index)
            outfile1.writelines(oneline + '\n')

    pre_process_input_file_list = ["raw_text.txt"]
    pre_process_output_file_list = ["pre_processed_data/pre_processed_text.txt"]

    for index in range(len(pre_process_input_file_list)):
        input_file_path = pre_process_input_file_list[index]
        output_file_path = pre_process_output_file_list[index]

        all_data = open(input_file_path, 'r').readlines()

        with open(output_file_path, 'w') as outfile:
            for line_index in range(len(all_data)):
                oneline = all_data[line_index]

                one_list = oneline.strip().split('|||')
                text_label = one_list[0].strip()

                if text_label not in label_dict.keys():
                    text_label = "Media and drama"

                try:
                    digit_label = label_dict[text_label]
                    out_one_line = str(digit_label) + " |||" + one_list[1]
                    outfile.writelines(out_one_line + '\n')
                except:
                    print("err at line: " + str(line_index))
                    print("err key: " + str(text_label))


def extract_word_cnt(file_name):
    global word_dict

    with open(file_name, 'r', encoding='utf-8') as infile:
        for oneline in infile.readlines():
            one_sentence = oneline.strip().split('|||')[1].strip()

            for one_word in one_sentence.split():
                word = one_word.strip().lower()
                word_dict[word] = 1


def save_subset_vector(word_dict):
    fin = io.open(word_embedding_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    hit_dict = {}

    with open(word_subset_file, 'w', encoding='utf-8') as outfile:
        for line in fin:
            tokens = line.rstrip().split(' ')
            one_word = tokens[0].lower()

            if (one_word in word_dict) and (one_word not in hit_dict):
                token_vec = list(map(float, tokens[1:]))
                token_vec_str = ""

                for element_index in range(len(token_vec)):
                    token_vec_str += " " + str(token_vec[element_index])

                outfile.writelines(str(one_word) + token_vec_str + "\n")
                hit_dict[one_word] = 1
    
    print("hit: " + str(len(hit_dict)))
    return hit_dict


def extract_vector_subset():
    extract_word_cnt("pre_processed_data/pre_processed_text.txt")

    print("\nTotal unique number of words all sets: " + str(len(word_dict)))

    hit_dict = save_subset_vector(word_dict)

    # miss_list = []
    # for one_key in word_dict:
    #     if one_key not in hit_dict:
    #         miss_list.append(one_key)
    
    # for index in range(len(miss_list)):
    #     print(miss_list[index].encode('utf-8'))
    #     if index > 10:
    #         break


def main():
    generate_mapping()
    extract_vector_subset()


if __name__ == "__main__":
    main()
