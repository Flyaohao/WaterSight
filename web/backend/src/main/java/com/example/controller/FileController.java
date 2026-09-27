package com.example.controller;

import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.io.FileUtil;
import cn.hutool.core.lang.Dict;
import cn.hutool.core.thread.ThreadUtil;
import cn.hutool.core.util.StrUtil;
import com.example.common.Result;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletResponse;
import java.io.OutputStream;
import java.net.URLEncoder;

/**
 * 文件接口
 */
@RestController
@RequestMapping("/files")
public class FileController {

    // 定义文件上传存储路径，使用系统属性获取当前工作目录，确保路径动态适配
    private static final String filePath = System.getProperty("user.dir") + "/files/";

    // 注入服务器端口配置，使用Spring框架的@Value注解，默认值为9090
    @Value("${server.port:9090}")
    private String port;

    // 注入服务器IP配置，使用Spring框架的@Value注解，默认值为localhost@Value("${ip:localhost}")
    @Value("${ip:localhost}")
    private String ip;

    /**
     * 文件上传
     */
    @PostMapping("/upload")
    public Result upload(MultipartFile file) {
        // 生成唯一后缀，用于区分不同的文件
        String flag;
        // 使用类对象作为锁，确保并发下flag的唯一性
        synchronized (FileController.class) {
            flag = System.currentTimeMillis() + "";
            ThreadUtil.sleep(1L);
        }
        String fileName = file.getOriginalFilename();
        try {
            // 检查并创建文件目录
            if (!FileUtil.isDirectory(filePath)) {
                FileUtil.mkdir(filePath);
            }
            // 文件存储形式：时间戳-文件名
            FileUtil.writeBytes(file.getBytes(), filePath + flag + "-" + fileName);  // ***/manager/files/1697438073596-avatar.png
            System.out.println(fileName + "--上传成功");

        } catch (Exception e) {
            System.err.println(fileName + "--文件上传失败");
        }
        // 构造文件访问路径
        String http = "http://" + ip + ":" + port + "/files/";
        // 返回文件的访问地址
        return Result.success(http + flag + "-" + fileName);  //  http://localhost:9090/files/1697438073596-avatar.png
    }


    /**
     * 富文本文件上传
     */
    @PostMapping("/editor/upload")
    public Dict editorUpload(MultipartFile file) {
        // 生成唯一后缀前缀，防止文件名重复
        String flag;
        synchronized (FileController.class) {
            flag = System.currentTimeMillis() + "";
            ThreadUtil.sleep(1L);
        }
        // 获取原始文件名
        String fileName = file.getOriginalFilename();
        try {
            // 检查并创建文件路径
            if (!FileUtil.isDirectory(filePath)) {
                FileUtil.mkdir(filePath);
            }
            // 文件存储形式：时间戳-文件名
            FileUtil.writeBytes(file.getBytes(), filePath + flag + "-" + fileName);  // ***/manager/files/1697438073596-avatar.png
            System.out.println(fileName + "--上传成功");

        } catch (Exception e) {
            System.err.println(fileName + "--文件上传失败");
        }
        // 构建文件访问路径
        String http = "http://" + ip + ":" + port + "/files/";
        // 返回上传结果，包括文件URL
        return Dict.create().set("errno", 0).set("data", CollUtil.newArrayList(Dict.create().set("url", http + flag + "-" + fileName)));
    }


    /**
     * 获取文件
     *
     * 根据提供的标志下载文件如果标志对应文件存在，则将文件作为附件返回
     *
     * @param flag 文件名标志，用于定位特定的文件
     * @param response HTTP响应对象，用于设置响应头和输出流以传输文件
     */
    @GetMapping("/{flag}")   //  1697438073596-avatar.png
    public void avatarPath(@PathVariable String flag, HttpServletResponse response) {
        OutputStream os;
        try {
            // 检查标志是否非空，以防止空指针异常
            if (StrUtil.isNotEmpty(flag)) {
                // 设置响应头，指示浏览器以附件形式下载文件，并编码文件名以防止中文名乱码问题
                response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode(flag, "UTF-8"));
                response.setContentType("application/octet-stream");
                // 读取文件字节流
                byte[] bytes = FileUtil.readBytes(filePath + flag);
                os = response.getOutputStream();
                // 将文件字节流写入HTTP响应输出流，以传输文件到客户端
                os.write(bytes);
                os.flush();
                os.close();
            }
        } catch (Exception e) {
            // 异常处理：输出错误信息，表示文件下载失败
            System.out.println("文件下载失败");
        }
    }

    /**
     * 删除指定的文件
     *
     * 本方法通过接收一个标志参数来确定要删除的文件，主要解决的是通过HTTP请求删除服务器上的文件的需求
     * 它使用了DELETE HTTP方法映射到"/{flag}"路径，其中flag是用于标识要删除的文件的参数
     *
     * @param flag 文件标识符，用于指定要删除的文件
     */
    @DeleteMapping("/{flag}")
    public void delFile(@PathVariable String flag) {
        // 使用FileUtil工具类删除拼接的文件路径
        FileUtil.del(filePath + flag);
        // 打印删除成功的信息，包含文件标识符
        System.out.println("删除文件" + flag + "成功");
    }


}
