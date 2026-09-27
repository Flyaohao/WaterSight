package com.example.entity;

/**
 * 角色用户父类，用于存储用户的账户信息。
 */
public class Account {
    /**
     * 用户唯一标识符。
     */
    private Integer id;

    /**
     * 用户名，用于登录系统。
     */
    private String username;

    /**
     * 用户的显示名称。
     */
    private String name;

    /**
     * 用户的密码，用于验证身份。
     */
    private String password;

    /**
     * 用户的角色标识，用于权限管理。
     */
    private String role;

    /**
     * 用户的新密码，用于修改密码时使用。
     */
    private String newPassword;

    /**
     * 用户的头像URL。
     */
    private String avatar;

    /**
     * 用户的认证令牌，用于会话管理。
     */
    private String token;

    /**
     * 获取用户唯一标识符。
     * @return 用户ID
     */
    public Integer getId() {
        return id;
    }

    /**
     * 设置用户唯一标识符。
     * @param id 用户ID
     */
    public void setId(Integer id) {
        this.id = id;
    }

    /**
     * 获取用户名。
     * @return 用户名
     */
    public String getUsername() {
        return username;
    }

    /**
     * 设置用户名。
     * @param username 用户名
     */
    public void setUsername(String username) {
        this.username = username;
    }

    /**
     * 获取用户的显示名称。
     * @return 显示名称
     */
    public String getName() {
        return name;
    }

    /**
     * 设置用户的显示名称。
     * @param name 显示名称
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取用户的密码。
     * @return 密码
     */
    public String getPassword() {
        return password;
    }

    /**
     * 设置用户的密码。
     * @param password 密码
     */
    public void setPassword(String password) {
        this.password = password;
    }

    /**
     * 获取用户的角色标识。
     * @return 角色标识
     */
    public String getRole() {
        return role;
    }

    /**
     * 设置用户的角色标识。
     * @param role 角色标识
     */
    public void setRole(String role) {
        this.role = role;
    }

    /**
     * 获取用户的新密码。
     * @return 新密码
     */
    public String getNewPassword() {
        return newPassword;
    }

    /**
     * 设置用户的新密码。
     * @param newPassword 新密码
     */
    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    /**
     * 获取用户的头像URL。
     * @return 头像URL
     */
    public String getAvatar() {
        return avatar;
    }

    /**
     * 设置用户的头像URL。
     * @param avatar 头像URL
     */
    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    /**
     * 获取用户的认证令牌。
     * @return 认证令牌
     */
    public String getToken() {
        return token;
    }

    /**
     * 设置用户的认证令牌。
     * @param token 认证令牌
     */
    public void setToken(String token) {
        this.token = token;
    }
}
