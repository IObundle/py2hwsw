#include "versat_crypto_tests.h"

#include "iob-uart16550.h"
#include "printf.h"

int VersatSimpleSHATests(){
  String content = STRING("LEN = 0\n"
                          "MSG = 00\n"
                          "MD = E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855\n"
                          "LEN = 256\n"
                          "MSG = 09FC1ACCC230A205E4A208E64A8F204291F581A12756392DA4B8C0CF5EF02B95\n"
                          "MD = 4F44C1C7FBEBB6F9601829F3897BFD650C56FA07844BE76489076356AC1886A4\n"
                          "LEN = 512\n"
                          "MSG = 5A86B737EAEA8EE976A0A24DA63E7ED7EEFAD18A101C1211E2B3650C5187C2A8A650547208251F6D4237E661C7BF4C77F335390394C37FA1A9F9BE836AC28509\n"
                          "MD = 42E61E174FBB3897D6DD6CEF3DD2802FE67B331953B06114A65C772859DFC1AA\n");

  TestState result = VersatCommonSHATests(content);

  if(result.earlyExit){
    printf("SHA early exit.\n");
    return 1;
  }

  printf("SHA: Passing:%d Total:%d\n",result.goodTests,result.tests);

  return (result.goodTests == result.tests) ? 0 : 1;
}

int VersatSimpleAESTests(){
  String content = STRING("COUNT = 7\n"
                           "KEY = 85405C4F0EBBE8F29228F02F1FF184E2F5E7857E8933C2A1D08F61ECB9B68111\n"
                           "PLAINTEXT = 0F5321DB6FD9D816D88E28183A739D90\n"
                           "CIPHERTEXT = 2AC6DE212DA0434BEA9CDD7332637307\n"
                           "COUNT = 8\n"
                           "KEY = F157285DB00E64C2791668A54493966E3039A19426605056B95B7EAC5106667D\n"
                           "PLAINTEXT = 3637F71F60A430322980349AD414FCFD\n"
                           "CIPHERTEXT = CA0A683E759C1312928FE01198F625BB\n"
                           "COUNT = 9\n"
                           "KEY = 44A2B5A7453E49F38261904F21AC797641D1BCD8DDEDD293F319449FE63B2948\n"
                           "PLAINTEXT = C91B8A7B9C511784B6A37F73B290516B\n"
                           "CIPHERTEXT = 05D51AF0E2B61E2C06CB1E843FEE3172\n");

  TestState result = VersatCommonAESTests(content);

  if(result.earlyExit){
    printf("AES early exit.\n");
    return 1;
  }

  printf("AES: Passing:%d Total:%d\n",result.goodTests,result.tests);

  return (result.goodTests == result.tests) ? 0 : 1;
}
