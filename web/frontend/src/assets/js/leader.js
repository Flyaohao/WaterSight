export function initParallax() {
    const bgLayers = document.querySelectorAll('.bg-layer');
    const viewportHeight = window.innerHeight;
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        const currentSection = Math.floor(scrolled / viewportHeight);
        const progress = (scrolled % viewportHeight) / viewportHeight;

        bgLayers.forEach((layer, index) => {
            if (index === currentSection) {
                // 当前图片
                layer.style.transform = `translateY(${progress * 100}%)`;
            } else if (index === currentSection + 1) {
                // 下一张图片
                layer.style.transform = `translateY(${(progress - 1) * 100}%)`;
            } else if (index === currentSection - 1) {
                // 上一张图片
                layer.style.transform = `translateY(${(1 + progress) * -100}%)`;
            } else {
                // 其他图片
                layer.style.transform = `translateY(${index > currentSection ? '100%' : '-100%'})`;
            }
        });
    });
}

// 修改后的水波纹效果函数
export function initRippleEffect() {
    // 创建一个容器来存放所有水波纹
    const rippleContainer = document.createElement('div');
    rippleContainer.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
  `;
    document.body.appendChild(rippleContainer);

    // 添加必要的CSS样式
    const style = document.createElement('style');
    style.textContent = `
    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.3);
      transform: translate(-50%, -50%);
      pointer-events: none;
      animation: ripple-effect 1s linear forwards;
    }

    .ripple::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      border-radius: 50%;
      box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.5);
      animation: ripple-inner 1s cubic-bezier(0.1, 0.1, 0.25, 1) forwards;
    }

    @keyframes ripple-effect {
      0% {
        width: 0;
        height: 0;
        opacity: 0.5;
      }
      100% {
        width: 500px;
        height: 500px;
        opacity: 0;
      }
    }

    @keyframes ripple-inner {
      0% {
        opacity: 1;
        transform: scale(0);
      }
      100% {
        opacity: 0;
        transform: scale(1);
      }
    }
  `;
    document.head.appendChild(style);

    // 添加点击事件监听器
    document.addEventListener('click', (event) => {
        const ripple = document.createElement('div');
        ripple.className = 'ripple';

        // 获取点击位置
        const x = event.clientX;
        const y = event.clientY;

        // 设置水波纹的位置
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        // 将水波纹添加到容器中
        rippleContainer.appendChild(ripple);

        // 动画结束后移除水波纹
        ripple.addEventListener('animationend', () => {
            try {
                if (ripple && rippleContainer.contains(ripple)) {
                    rippleContainer.removeChild(ripple);
                }
            } catch (error) {
                console.log('Ripple already removed');
            }
        });

        // 安全移除机制
        setTimeout(() => {
            try {
                if (ripple && rippleContainer.contains(ripple)) {
                    rippleContainer.removeChild(ripple);
                }
            } catch (error) {
                console.log('Ripple already removed');
            }
        }, 1100); // 稍微比动画时长长一点
    });
}