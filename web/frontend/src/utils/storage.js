/**
 * 本地存储工具类
 */
export default {
  // 设置本地存储
  set(key, value) {
    if (typeof value === 'object') {
      value = JSON.stringify(value)
    }
    localStorage.setItem(key, value)
  },

  // 获取本地存储
  get(key) {
    const value = localStorage.getItem(key)
    try {
      return JSON.parse(value)
    } catch (e) {
      return value
    }
  },

  // 移除本地存储
  remove(key) {
    localStorage.removeItem(key)
  },

  // 清空本地存储
  clear() {
    localStorage.clear()
  },

  // 获取本地存储长度
  length() {
    return localStorage.length
  },

  // 获取本地存储的所有key
  keys() {
    const keys = []
    for (let i = 0; i < localStorage.length; i++) {
      keys.push(localStorage.key(i))
    }
    return keys
  }
} 