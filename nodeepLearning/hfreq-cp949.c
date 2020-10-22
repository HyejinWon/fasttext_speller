//---------------------------------------------------------
// KS�ϼ��� �ѱ�-���� ������ ���α׷� -- cp949
//	usage: a.exe < test.txt
// <����> �Է����� test.txt�� �ѱ��ڵ�: KS�ϼ���
//  --> UTF-8 ���ڵ� ������ iconv�� �̿��Ͽ� cp949�� ��ȯ!
//  	$ iconv -f utf-8 -t cp949 in.txt > out.txt
// 2020�� 9�� 12��, ���δ��б� ����Ʈ�����к� ���½�
//---------------------------------------------------------
#include <stdio.h>

int freq[256][256]; // cp949 ������

void put_freq_ASCII() {
	int i, j, n=0, sum=0;

	printf("�� ��� -- ASCII ����\n");
	for (i = 0; i < 256; i++) {
		if (freq[0][i]) {
			printf("\t");
			if (i == 0x09 || i == 0x0a || i == 0x0d) {
				if (i == 0x09)	// tab ����
					printf("f[\\t] = %d\n", freq[0][i]);
				else if (i == 0x0a)	// LF ����
					printf("f[\\n] = %d\n", freq[0][i]);
				else if (i == 0x0d)	// CR ����
					printf("f[\\r] = %d\n", freq[0][i]);
			} else printf("f[%c] = %d\n", i, freq[0][i]);

			n++; sum += freq[0][i];
		}
	}

	printf("num_of_chars= %d, sum_of_freq[i]= %d\n\n", n, sum);
}

void put_freq_KSC5601_hangul() {
	int i, j, n=0, sum=0;

	printf("�� ��� -- KS�ϼ��� �ѱ� 2350��\n");
	for (i=0xB0; i <= 0xC8; i++) {
		for (j=0xA1; j <= 0xFE; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}
	}

	printf("num_of_chars= %d, sum_of_freq[i]= %d\n\n", n, sum);
}

void put_freq_KSC5601_hanja() {
	int i, j, n=0, sum=0;

	printf("�� ��� -- KS�ϼ��� ���� 4888��\n");
	for (i=0xCA; i <= 0xFD; i++) {
		for (j=0xA1; j <= 0xFE; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}
	}

	printf("num_of_chars= %d, sum_of_freq[i]= %d\n\n", n, sum);
}

void put_freq_KSC5601_94x94() {
	int i, j, n=0, sum=0;

	printf("�� ��� -- KS�ϼ��� ��ü 8836��(=94x94)\n");
	for (i=0xA1; i <= 0xFE; i++) {
		for (j=0xA1; j <= 0xFE; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}
	}

	printf("num_of_chars= %d, sum_of_freq[i]= %d\n\n", n, sum);
}


// [81~A0][41~5A,61~7A,81~FE] : 32x(26+26+126)
// [A1~C5][41~5A,61~7A,81~A0] : 37x(26+26+32)
// C6 [41-52] : 18��
void put_freq_cp949_8822()
{
	int i, j, n=0, sum=0;

	printf("�� ��� -- cp949�� ���ǵ� 8822�� �����\n");
	// ���⿡ �ڵ带 �ϼ��Ͻÿ�
	for (i=0x81; i <= 0xA0; i++) {
		for (j=0x41; j <= 0x5A; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}

		for (j=0x81; j <= 0xFE; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}

		for (j=0x61; j <= 0x7A; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}
	}

	for (i=0xA1; i <= 0xC5; i++) {
		for (j=0x41; j <= 0x5A; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}

		for (j=0x81; j <= 0xFE; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}

		for (j=0x61; j <= 0x7A; j++) {
			if (freq[i][j]) {	// �� 0�� ��� ����!
				printf("\tf[%c%c] = %d\n", i, j, freq[i][j]);
				n++; sum += freq[i][j];
			}
		}
	}

	for (j=0x41; j <= 0x52; j++) {
		if (freq[0xC6][j]) {	// �� 0�� ��� ����!
			printf("\tf[%c%c] = %d\n", 0xC6, j, freq[0xC6][j]);
			n++; sum += freq[0xC6][j];
		}
	}
		
	printf("num_of_chars= %d, sum_of_freq[i]= %d\n\n", n, sum);
}

int main()
{
	int ch, i, j, c1, c2;

	while ((c1 = getchar()) != EOF) {
		if (c1 < 128)	// SBCS -- ASCII ����
			freq[0][c1]++;
		else {	// DBCS -- cp949
			c2 = getchar();
			freq[c1][c2]++;
		}
	}

	put_freq_ASCII();
	put_freq_KSC5601_hangul();	// KS�ϼ��� �ѱ� 2350��
	//put_freq_KSC5601_hanja();	// KS�ϼ��� ���� 4888��
	
	//put_freq_KSC5601_94x94();	// KS�ϼ��� ��ü 8836��

	//put_freq_cp949_8822();	// cp949�� ���ǵ� 8822�� �����

	return 0;
}
