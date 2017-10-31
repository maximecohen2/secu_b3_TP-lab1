import hashlib
import time


shadowFile = 'shadow.txt'
DictionaryFile = 'dico_mini_fr.txt'
outputFile = 'decrypted_passwords.txt'

type_crypt = {
	1:hashlib.md5,
	5:hashlib.sha256,
	6:hashlib.sha512
}

def get_passwords():
	userDictionary = {}
	try:
		pass_file = open(shadowFile, "r")
		lines = pass_file.readlines()
		for line in lines:
			tab = line.split(':')
			if len(tab) > 1 and tab[1] not in ['!','*']:
				user = tab[0]
				crypt = tab[1].split('$')
				userDictionary[user] = [crypt[1], crypt[2]]
				print('[*] Cracking Password For =  {}: {},{}'.format(user, crypt[1], crypt[2]))
		return (userDictionary)
	except FileNotFoundError:
		print("Error: Can't open file")

def decrypt_shadow(userDictionary):
	passwordDictionary = {}
	try:
		dictionary_file = open(DictionaryFile, "r")
		timeStart = time.time()
		for line in dictionary_file:
			password = line.replace("\n", "")
			for user, shadow in userDictionary.items():
				if int(shadow[0]) in type_crypt.keys():
					crypt = type_crypt[int(shadow[0])]
					crypt_password = crypt(password.encode('utf-8')).hexdigest()
					if (crypt_password == shadow[1]):
						timeEnd = time.time()
						passwordDictionary[user] = [password , float(timeEnd - timeStart)]
						print ("Found password: \"{}\" for user {}".format(password, user))
		return (passwordDictionary)

	except FileNotFoundError:
		print("Error: Can't open file")

def file_write(passwordDictionary):
	try:
		output = open(outputFile, "w")
		for user ,password in passwordDictionary.items():
			out = "user: {}, password: {}, time: {}'s".format(user, password[0], round(password[1], 4))
			output.write(out + '\n')

	except FileNotFoundError:
		print("Error: Can't write file")

def main():
	userDictionary = get_passwords()
	passwordDictionary = decrypt_shadow(userDictionary)
	file_write(passwordDictionary)

if __name__ == '__main__':
	main()