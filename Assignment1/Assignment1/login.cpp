#include <cstdio>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
using namespace std;

void login1(char * input1, char * input2) {
	struct {
		char username[25];
		char password[25];
		char canary;		
		char good_username[25];
		char good_password[25];
		char goodcanary;
	} v;
	v.canary = 'b';
	v.goodcanary = 'b';

	//read correct username and password
	FILE * fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username)-1] = '\0';
	v.good_password[strlen(v.good_password)-1] = '\0';
	strcpy(v.username, input1);
	strcpy(v.password, input2);

	//terminate strings properly for strcmp
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	//check canary and login success
	if (v.canary != v.goodcanary) {
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0) printf("Login successful!\n");
/*
	printf("v.username: %s ", v.username);
	printf("v.password: %s ", v.password);
	printf("v.canary: %s ", v.canary);
	printf("v.good_username: %s ", v.good_username);
	printf("v.good_password: %s ", v.good_password);
	printf("v.goodcanary: %s ", v.goodcanary);
*/
	cout << "v.username: " << v.username << endl;
	cout << "v.password: " << v.password << endl;
	cout << "v.canary: " << v.canary << endl;
	cout << "v.good_username: " << v.good_username << endl;
	cout << "v.good_password: " << v.good_password << endl;
	cout << "v.goodcanary: " << v.goodcanary << endl;
}

void login2(char * input1, char * input2) {
	struct {
		int32_t goodcanary; //these are integers now instead of characters
		char password[25];
		int32_t canary;
		char good_username[25];
		char good_password[25];
		char username[25];
	} v;
	v.canary = 'b';
	v.goodcanary = 'b';

	//read correct username and password
	FILE * fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username)-1] = '\0';
	v.good_password[strlen(v.good_password)-1] = '\0';

	//load username
	strcpy(v.username, input1);

	//set up "random" canary
	//for real code, it is often possible to read or predict the true value of canaries
	//this example reflects that phenomenon, though it is fake
	v.goodcanary =  v.username[1]*256*256*257 + (v.username[0]-20)*256 + 67;
	v.canary = v.goodcanary;
	cout << "v.goodcanary: " << (char)v.goodcanary << endl;
	
	unsigned char bytes[4];
	int32_t n = v.goodcanary;
	bytes[0] = (n >> 24) & 0xFF;
	bytes[1] = (n >> 16) & 0xFF;
	bytes[2] = (n >> 8) & 0xFF;
	bytes[3] = n & 0xFF;
	cout << bytes[0] << bytes[1] << bytes[2] << bytes[3] << endl;

	//load password
	strcpy(v.password, input2);

	//terminate strings properly for strcmp
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	cout << "v.username: " << v.username << endl;
	cout << "v.password: " << v.password << endl;
	cout << "v.canary: " << v.canary << endl;
	unsigned char nbytes[7];

	/*
	int32_t n2 = v.canary;

	nbytes[0] = (n2 >> 48) & 0xFF;
	nbytes[1] = (n2 >> 40) & 0xFF;
	nbytes[2] = (n2 >> 32) & 0xFF;
	nbytes[3] = (n2 >> 24) & 0xFF;
	nbytes[4] = (n2 >> 16) & 0xFF;
	nbytes[5] = (n2 >> 8) & 0xFF;
	nbytes[6] = n2 & 0xFF;
	*/
	cout << bytes[0] << bytes[1] << bytes[2] << bytes[3]
		<< bytes[4] << bytes[5] << bytes[6] << endl;
	cout << "v.good_username: " << v.good_username << endl;
	cout << "v.good_password: " << v.good_password << endl;
	cout << "v.goodcanary: " << v.goodcanary << endl;
	
	//check canary and login success
	if (v.canary != v.goodcanary) {
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0) printf("Login successful!\n");

}

void login3(char * input1, char * input2) {
	struct {
		int32_t goodcanary;
		char username[25];
		char password[25];
		int32_t canary;
		char good_username[25];
		char good_password[25];
	} v;
	srand(time(NULL));
	v.goodcanary = rand();
	v.canary = v.goodcanary;

	//read correct username and password
	FILE * fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username)-1] = '\0';
	v.good_password[strlen(v.good_password)-1] = '\0';
	strcpy(v.username, input1);
	//let's load v.password carefully. we only want valid characters.
	int written_char = 0;
	int warn_user = 0;
	int ind = 0;

	cout << "strlen(v.password) before written: " << strlen(v.password) << endl;
	cout << "v.password before written: " << v.password << endl;
	while (written_char < 25) { //don't write too much
		int c = (int)input2[ind];

		if (written_char == 23)
			cout << "written_char = 23, and now c is " << input2[ind] << endl;
		if (written_char == 24)
			cout << "written_char = 24, and c now is " << c << " and ind is " << ind << endl;

		if (c == 0 || (c >= 48 && c <= 57) || (c >= 65 && c <= 90) || (c >= 97 && c <= 122) ) {
			//this is an okay character. load it
			v.password[ind] = (char)c;
			written_char += 1;
		}
		else if (c == 9) {//sometimes user hits tab by accident. let's turn it into a null.
			v.password[ind] = 0;
			written_char += 1;
		}
		else {//a strange character! let's warn the user, but don't load it
			warn_user = 1;
		}
		if (c == 0) {//reached end of string, terminate
			break;
		}
		ind += 1;
	}
	if (warn_user == 1) {
		printf("Invalid characters found and skipped. Did you type your password correctly?\n");
	}

	//terminate strings properly
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	cout << "v.username: " << v.username << endl;
	cout << "v.password: " << v.password << endl;
	cout << "v.good_username: " << v.good_username << endl;
	cout << "v.good_password: " << v.good_password << endl;
	cout << "v.canary: " << v.canary << endl;
	cout << "v.goodcanary: " << v.goodcanary << endl;
	
	unsigned char bytes[4];
	int32_t n = v.canary;
	bytes[0] = (n >> 24) & 0xFF;
	bytes[1] = (n >> 16) & 0xFF;
	bytes[2] = (n >> 8) & 0xFF;
	bytes[3] = n & 0xFF;
	cout << "canary: " << bytes[0] << bytes[1] << bytes[2] << bytes[3] << endl;
	
	unsigned char nbytes[4];
	int32_t n2 = v.goodcanary;
	nbytes[0] = (n2 >> 24) & 0xFF;
	nbytes[1] = (n2 >> 16) & 0xFF;
	nbytes[2] = (n2 >> 8) & 0xFF;
	nbytes[3] = n2 & 0xFF;
	cout << "goodcanary: " << nbytes[0] << nbytes[1] << nbytes[2] << nbytes[3] << endl;
	//check canary and login success
	if (v.canary != v.goodcanary) {
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0) printf("Login successful!\n");

}

int main(int argc, char* argv[]) {
	char helpstr[] = "Use: login -? <username> <password> or Use: login -l <filename>\nOptions are: -i, -j, -k, -l (see assignment)\n";
	if (argc < 3) {
		printf("%s\n", helpstr);
		return -1;
	}

	if( access( "password.txt", F_OK ) == -1 ) {
		printf("password.txt not found; please download it and put it in this directory.\n");
		return -1;
	}

	if (strlen(argv[1]) < 2) {
		printf("%s\n", helpstr);
		return -1;
	}

	switch(argv[1][1]) {
		case 'i':
			if (argc < 4) {
				break;
			}
			login1(argv[2], argv[3]);
			break;
		case 'j':
			if (argc < 4) {
				break;
			}
			login2(argv[2], argv[3]);
			break;
		case 'k':
			if (argc < 4) {
				break;
			}
			login3(argv[2], argv[3]);
			break;
		default:
			printf("%s\n", helpstr);
			return -1;
	}
	return 0;
}
