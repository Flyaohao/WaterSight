package com.example.common.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import javax.annotation.Resource;

@Configuration
public class WebConfig implements  WebMvcConfigurer {

    @Resource
    private JwtInterceptor jwtInterceptor;

    /**
     * 注册RestTemplate Bean，用于HTTP请求
     */
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    /**
     * 配置CORS跨域
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .maxAge(3600);
    }

    // 加自定义拦截器JwtInterceptor，设置拦截规则
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 注册自定义拦截器 jwtInterceptor，并设置拦截的 URL 路径模式
        registry.addInterceptor(jwtInterceptor).addPathPatterns("/**")
                // 排除根路径，即不拦截访问根路径的请求
                .excludePathPatterns("/")
                // 排除登录路径，即不拦截访问登录页面的请求
                .excludePathPatterns("/login")
                // 排除管理员登录路径
                .excludePathPatterns("/admin")
                // 排除注册路径，即不拦截访问注册页面的请求
                .excludePathPatterns("/register")
                // 排除文件上传和下载的路径，即不拦截访问文件相关操作的请求
                .excludePathPatterns("/files/**")
                // 排除图像增强相关接口
                .excludePathPatterns("/api/enhance/**")
                // 排除公开接口
                .excludePathPatterns("/blog/selectPage")
                .excludePathPatterns("/blog/selectTop")
                .excludePathPatterns("/activity/selectPage")
                .excludePathPatterns("/activity/selectTop")
                .excludePathPatterns("/category/selectAll")
                .excludePathPatterns("/tag/getHotTags")
                .excludePathPatterns("/notice/selectAll")
                .excludePathPatterns("/user/updateBrowseRole")
                .excludePathPatterns("/user/login")
                .excludePathPatterns("/error");
    }

}