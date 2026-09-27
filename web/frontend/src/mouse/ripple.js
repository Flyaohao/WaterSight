
export default {
    bind(el) {
        // 强制容器样式
        el.style.position = 'relative'
        el.style.overflow = 'hidden'
        el.style.cursor = 'pointer'  // 为div添加手型光标

        // 创建涟漪动画方法
        const createRipple = (e) => {
            // 清理旧涟漪
            const oldRipples = el.getElementsByClassName('ripple-effect')
            while(oldRipples.length > 0) {
                oldRipples[0].remove()
            }

            // 计算涟漪位置
            const rect = el.getBoundingClientRect()
            const ripple = document.createElement('div')
            const size = Math.max(rect.width, rect.height)
            const x = e.clientX - rect.left - size/2
            const y = e.clientY - rect.top - size/2

            // 设置涟漪样式
            ripple.className = 'ripple-effect'
            ripple.style.width = ripple.style.height = `${size}px`
            ripple.style.left = `${x}px`
            ripple.style.top = `${y}px`

            // 添加动画结束自动移除
            ripple.addEventListener('animationend', () => {
                ripple.remove()
            })

            el.appendChild(ripple)
        }

        // 绑定点击事件
        el._rippleHandler = createRipple
        el.addEventListener('click', el._rippleHandler)
    },

    unbind(el) {
        // 清理事件监听
        el.removeEventListener('click', el._rippleHandler)
        delete el._rippleHandler
    }
}