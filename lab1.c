#include <stdio.h>

int main() {
	float c_temp;
	float f_temp;
	printf("화씨 온도를 입력하세요 : ");
	scanf("%f",&f_temp);
	c_temp = (f_temp - 32.0) * 5.0 / 9.0;
	printf("섭씨 온도는 %.2f도 입니다", c_temp);

	return 0;
}