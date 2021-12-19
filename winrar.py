import os
from bitarray import bitarray

window_size = 64 # razmer skol'zyashchego okna
buffer_size = 15 # dlina sovpadeniya ne boleye 4 bit

def delete_last_line(file_path): # Funktsiya udaleniya posledney stroki, v kotoroy v arkhivirovannom fayle khranitsya rasshireniye starogo fayla
    file = open(file_path, "rb+")
    file_extension = file.readlines()[-1].decode()
    for i in range(len(file_extension)+1):
        file.seek(-1, os.SEEK_END)
        file.truncate()
    return file_extension

def compress(file_path):
	filename, file_extension = os.path.splitext(file_path)
	output_file_path=f"{filename}Compressed.txt" # Imya fayla, kotoryy budet v itoge vyveden
	data = None
	i = 0
	buffer = bitarray(endian='big')# Predstavlyayem bufer kak posledovatel'nost' bit

	with open(file_path, 'rb') as input_file: # Schityvayem fayl
		data = input_file.read()

	while i < len(data):
		match = findLongestMatch(data, i)
		if match: # Dobavlyayem 1 bitovyy flag, zatem 12 bit dlya rasstoyaniya i 4 bita dlya dliny sovpadeniya.
			(MatchDistance, MatchLength) = match
			buffer.append(True)
			buffer.frombytes(bytes([MatchDistance >> 4]))
			buffer.frombytes(bytes([((MatchDistance & 0xf) << 4) | MatchLength]))
			i += MatchLength
		else: # Yesli ne naydeno ni odnogo poleznogo sovpadeniya, dobavim 0-bitnyy flag, a zatem 8-bitnyy dlya simvola
			buffer.append(False)
			buffer.frombytes(bytes([data[i]]))
			i += 1
            
	buffer.fill() # Zapolnyayem bufer nulyami yesli kolichestvo bit ne kratno 8

	with open(output_file_path, 'wb') as output_file: # Zapisat' szhatyye dannyye v fayl
		output_file.write(buffer.tobytes())        
		output_file.write(b'\n'+file_extension.encode()) # Zapishem rasshireniye iznachal'nogo fayla v szhatyye dannyye
	return buffer   

def decompress(file_path):
    filename, file_extension = os.path.splitext(file_path)
    data = bitarray(endian='big')
    output_buffer = []

    with open(file_path, 'rb') as input_file: # Schityvayem fayl
        file_extension = delete_last_line(file_path)
        data.fromfile(input_file)

    while len(data) >= 9: # Realizatsiya algoritma LZ77
    	flag = data.pop(0)
    	if not flag:
    		byte = data[0:8].tobytes()
    		output_buffer.append(byte)
    		del data[0:8]
    	else:
    		byte1 = ord(data[0:8].tobytes())
    		byte2 = ord(data[8:16].tobytes())

    		del data[0:16]
    		distance = (byte1 << 4) | (byte2 >> 4)
    		length = (byte2 & 0xf)

    		for i in range(length):
    			output_buffer.append(output_buffer[-distance])
    out_data =  b''.join(output_buffer)
    output_file_path=(f"{filename}Decompressed{file_extension}")
    with open(output_file_path, 'wb') as output_file:
    	output_file.write(out_data)
    return out_data
    
def findLongestMatch(data, current_position):
	# Nakhodit samoye dlinnoye sovpadeniye s podstrokoy, nachinaya s current_position v 
    # predvaritel'nom bufere iz okna istorii
	end_of_buffer = min(current_position + buffer_size, len(data) + 1)
	best_match_distance = -1
	best_match_length = -1
	for j in range(current_position + 2, end_of_buffer):
		start_index = max(0, current_position - window_size)
		substring = data[current_position:j]
		for i in range(start_index, current_position):
			repetitions = len(substring) // (current_position - i)
			last = len(substring) % (current_position - i)
			matched_string = data[i:current_position] * repetitions + data[i:i+last]
			if matched_string == substring and len(substring) > best_match_length:
				best_match_distance = current_position - i 
				best_match_length = len(substring)
	if best_match_distance > 0 and best_match_length > 0:
		return (best_match_distance, best_match_length)
	return None