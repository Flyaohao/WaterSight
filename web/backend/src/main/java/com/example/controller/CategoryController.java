package com.example.controller;

import com.example.common.Result;
import com.example.entity.Category;
import com.example.service.CategoryService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;
import java.util.List;

/**
 * 博客分类前端操作接口
 **/
@RestController
@RequestMapping("/category")
public class CategoryController {

    @Resource
    private CategoryService categoryService;

    /**
     * 新增分类
     */
    @PostMapping("/add")
    public Result add(@RequestBody Category category) {
        categoryService.add(category);
        return Result.success();
    }

    /**
     * 删除分类
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        categoryService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除分类
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {
        categoryService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改分类
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody Category category) {
        categoryService.updateById(category);
        return Result.success();
    }

    /**
     * 根据ID查询分类
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        Category category = categoryService.selectById(id);
        return Result.success(category);
    }

    /**
     * 查询所有分类
     */
    @GetMapping("/selectAll")
    public Result selectAll(@RequestParam(required = false) String role) {
        Category category = new Category();
        if (role != null && !role.isEmpty()) {
            category.setRole(role);
        }
        List<Category> list = categoryService.selectAll(category);
        return Result.success(list);
    }

    /**
     * 根据角色查询分类
     */
    @GetMapping("/selectByRole")
    public Result selectByRole(@RequestParam String role) {
        List<Category> list = categoryService.selectByRole(role);
        return Result.success(list);
    }

    /**
     * 分页查询分类
     */
    @GetMapping("/selectPage")
    public Result selectPage(Category category,
                           @RequestParam(defaultValue = "1") Integer pageNum,
                           @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<Category> page = categoryService.selectPage(category, pageNum, pageSize);
        return Result.success(page);
    }

    /**
     * 初始化默认分类
     */
    @PostMapping("/initDefaultCategories")
    public Result initDefaultCategories() {
        try {
            // 先删除所有现有分类
            categoryService.deleteAll();
            
            // 科研人员分类
            String[] researcherCategories = {
                "水下图像", "水下机器人", "海洋环境监测", "水下通信与传感",
                "深海生物学", "海洋能源开发", "水下考古与地质勘探"
            };
            
            // 业余爱好者分类
            String[] hobbyistCategories = {
                "摄影", "潜水", "游泳", "水产养殖", "美食"
            };

            // 添加科研人员分类
            for (String name : researcherCategories) {
                Category category = new Category();
                category.setName(name);
                category.setRole("RESEARCHER");
                categoryService.add(category);
            }

            // 添加业余爱好者分类
            for (String name : hobbyistCategories) {
                Category category = new Category();
                category.setName(name);
                category.setRole("HOBBYIST");
                categoryService.add(category);
            }

            return Result.success("分类初始化成功");
        } catch (Exception e) {
            return Result.error("500", "分类初始化失败：" + e.getMessage());
        }
    }
}