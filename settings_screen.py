import os
import persistence
import torch


def show():
    while True:
        os.system('cls||clear')
        json_settings = persistence.load()
        print('model:', json_settings['selected_model'])
        print('hardware:', json_settings['selected_hw'])
        detect_gpu()

        print("0. Back")
        print("1. Select translation model")
        print("2. Select hardware")
        choice = input("Select: ")
        os.system('cls||clear')

        if choice == '0':
            return persistence.load()

        elif choice == '1':
            print("1. NLLB200")
            print("2. small100")
            choice = input("Select: ")
            if choice == '1':
                persistence.set(json_settings, 'selected_model', 'NLLB200')
            elif choice == '2':
                persistence.set(json_settings, 'selected_model', 'small100')

        elif choice == '2':
            print("1. cuda GPU")
            print("2. CPU")
            choice = input("Select: ")
            if choice == '1':
                persistence.set(json_settings, 'selected_hw', 'cuda')
            elif choice == '2':
                persistence.set(json_settings, 'selected_hw', 'cpu')


def detect_gpu():
    # todo: hw vs drivers
    if torch.cuda.is_available():
        print("CUDA is available:")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("No CUDA GPU detected.")
    print('---------------\n')
