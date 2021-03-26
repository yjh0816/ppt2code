#include <stdio.h>

int main() {
	float c_temp;
	float f_temp;
	printf("ȭ�� �µ��� �Է��ϼ��� : ");
	scanf("%f",&f_temp);
	c_temp = (f_temp - 32.0) * 5.0 / 9.0;
	
	printf("���� �µ��� %.2f�� �Դϴ�", c_temp);

	return 0;
}