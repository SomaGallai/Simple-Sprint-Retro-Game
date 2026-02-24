#!/bin/bash

#Welcome screen
clear
echo "Hey There, Team!"
echo -e "\nLet's Play a game\n\n\n"

#Define the file containing questions
questions_file="questions.txt"

#Declare associative array to hold questions
declare -A questions

while read -r line; do
    #Check if the line is a title
    if [[ $line == \#* ]]; then
        current_title="${line:1}" #Remove the '#' char
    elif [[ $line == -* ]]; then #It's a question if it has '-' char at start
        questions[$current_title]+="${line}"
    fi
done < "$questions_file"

select_title() {
    for val in "${!questions[@]}"; do
        echo "$iteration.$val" #Output the question types
        iteration=$((iteration + 1)) #Get the amount of questions type
    done

    #Add option to exit gracefully
    echo "$iteration.Exit"

    #Ask for user input for title selection
    echo -n "Please select a question type:"
    read -r answer

    #Validate the user input
    if [[ $answer == $iteration ]]; then
        clear
        echo -e "\n\n\nBye, Team!\n\n\n"
        exit 1
    elif [[ $answer -lt $iteration ]] && [[ $answer -gt 0 ]]; then
        selected_title=$answer
    else
        clear
        echo "An error has occured:"
        echo -e "\nUncorrect selection, try again! \n\n\n"
    fi
}

show_random_question() {
    local selected_option=$1
    iteration=1
    question_key=""

    #Select a random number based on array size
    local index=0
    while [[ $index == 0 ]]; do
        index=$((RANDOM % ${#questions[@]}))
    done

    #Get the key from array
    for val in "${!questions[@]}"; do
        if [[ $selected_option == $iteration ]]; then
            question_key=$val
            break
        elif [[ $selected_option != $iteration ]]; then
            iteration=$((iteration + 1))
        fi
    done

    #Splice the array questions with '-' char
    question_value=$(echo ${questions[$question_key]} | tr "-" "\n")

    while read -r line; do
        if [[ $index == 0 ]]; then
            clear
            echo "QUESTION: "
            echo -e "\n $line \n\n\n"
            break
        else
            index=$((index - 1))
        fi
    done <<<$question_value
}

#Main loop
while true; do
    selected_title=0

    while [[ $selected_title == 0 ]]; do
        current_title=""
        iteration=1

        select_title
    done

    show_random_question "$selected_title"
done