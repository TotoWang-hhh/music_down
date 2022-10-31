// 本程序可以获取作者的收藏内容
//请不要随意传播该代码，因为内有重要账户信息！

$fp = fopen('https://cloudmusic-api.txm.world/login/?email=***&md5_password=***', 'r');
print_r(stream_get_meta_data($fp));
fclose($fp);

$cookie = json_decode(stream_get_meta_data($fp)) -> cookie;

echo $cookie;