package com.example.mapper;

import com.example.entity.Follow;
import com.example.entity.User;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface FollowMapper {

    // 添加关注关系
    @Insert("INSERT INTO follow (follower_id, followed_id, create_time) VALUES (#{followerId}, #{followedId}, now())")
    void insert(Follow follow);

    // 删除关注关系
    @Delete("DELETE FROM follow WHERE follower_id = #{followerId} AND followed_id = #{followedId}")
    void delete(Follow follow);

    // 检查是否已经关注
    @Select("SELECT COUNT(*) FROM follow WHERE follower_id = #{followerId} AND followed_id = #{followedId}")
    int checkFollow(Integer followerId, Integer followedId);

    // 获取关注列表(某用户关注的人)
    @Select("SELECT u.*, (SELECT COUNT(*) FROM follow f2 WHERE f2.follower_id = #{userId} AND f2.followed_id = u.id) as isFollowing "
            + "FROM user u "
            + "JOIN follow f ON u.id = f.followed_id "
            + "WHERE f.follower_id = #{userId} "
            + "ORDER BY f.create_time DESC "
            + "LIMIT #{offset}, #{pageSize}")
    List<User> getFollows(Integer userId, Integer offset, Integer pageSize);

    // 获取粉丝列表(关注某用户的人)
    @Select("SELECT u.*, (SELECT COUNT(*) FROM follow f2 WHERE f2.follower_id = #{userId} AND f2.followed_id = u.id) as isFollowing "
            + "FROM user u "
            + "JOIN follow f ON u.id = f.follower_id "
            + "WHERE f.followed_id = #{userId} "
            + "ORDER BY f.create_time DESC "
            + "LIMIT #{offset}, #{pageSize}")
    List<User> getFans(Integer userId, Integer offset, Integer pageSize);

    // 统计关注总数
    @Select("SELECT COUNT(*) FROM follow WHERE follower_id = #{userId}")
    int countFollows(Integer userId);

    // 统计粉丝总数
    @Select("SELECT COUNT(*) FROM follow WHERE followed_id = #{userId}")
    int countFans(Integer userId);

    // 增加用户的关注计数
    @Update("UPDATE user SET follow_count = follow_count + 1 WHERE id = #{userId}")
    void increaseFollowCount(Integer userId);

    // 减少用户的关注计数
    @Update("UPDATE user SET follow_count = follow_count - 1 WHERE id = #{userId}")
    void decreaseFollowCount(Integer userId);

    // 增加用户的粉丝计数
    @Update("UPDATE user SET fans_count = fans_count + 1 WHERE id = #{userId}")
    void increaseFansCount(Integer userId);

    // 减少用户的粉丝计数
    @Update("UPDATE user SET fans_count = fans_count - 1 WHERE id = #{userId}")
    void decreaseFansCount(Integer userId);
}
