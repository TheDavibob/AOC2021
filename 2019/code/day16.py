import numpy as np

import common


def to_int_list(int_str):
    return [int(s) for s in int_str]


def brute_fft(int_list):
    output = []
    base_pattern = [1, 0, -1, 0]
    for i in range(len(int_list)):
        counter = 0
        cumulation = 0
        for j, old_int in enumerate(int_list[i:]):
            cumulation += old_int * base_pattern[counter]
            if (j+1) % (i+1) == 0:
                counter += 1
                counter %= 4

        output.append(int(str(cumulation)[-1]))
    return output


def brute_repeat_fft(int_list, n):
    current = int_list
    for _ in range(n):
        current = brute_fft(current)

    return current


def cheeky_fft(int_list):
    # This is valid for the second half of any integer list
    return np.mod(np.cumsum(int_list[::-1]), 10)[::-1]


if __name__ == "__main__":
    input = [int(s) for s in str(59791875142707344554745984624833270124746225787022156176259864082972613206097260696475359886661459314067969858521185244807128606896674972341093111690401527976891268108040443281821862422244152800144859031661510297789792278726877676645835805097902853584093615895099152578276185267316851163313487136731134073054989870018294373731775466754420075119913101001966739563592696702233028356328979384389178001923889641041703308599918672055860556825287836987992883550004999016194930620165247185883506733712391462975446192414198344745434022955974228926237100271949068464343172968939069550036969073411905889066207300644632441054836725463178144030305115977951503567)]
    common.part(1, int("".join(str(s) for s in brute_repeat_fft(input, 100)[:8])))

    # The initial point is quite late, which helps matters
    initial_index = int("".join(str(s) for s in input[:7]))
    offset_from_end = (10000 * len(input) - 5979187)
    reps_required = (offset_from_end // len(input)) + 1
    new_input = (reps_required * input)[-offset_from_end:]
    for _ in range(100):
        new_input = cheeky_fft(new_input)
    common.part(2, int("".join(str(s) for s in new_input[:8])))

