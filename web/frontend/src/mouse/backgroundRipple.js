// backgroundRipple.js
import _ from "lodash";

export default {
  mounted(el) {
    const container = document.createElement("div");
    container.className = "local-ripple-container";
    document.body.appendChild(container);

    let isActive = true;
    let lastTime = 0;

    // 存储事件处理函数的引用
    const mouseenterHandler = () => {
      isActive = true;
    };
    const mouseleaveHandler = () => {
      isActive = false;
    };

    const createRipple = (e) => {
      if (!isActive) return;

      const now = Date.now();
      if (now - lastTime < 50) return;
      lastTime = now;

      const rect = el.getBoundingClientRect();
      if (
        e.clientX < rect.left ||
        e.clientX > rect.right ||
        e.clientY < rect.top ||
        e.clientY > rect.bottom
      ) {
        return;
      }

      const ripple = document.createElement("div");
      ripple.className = "local-ripple";

      // 使用 pageX/pageY 代替 clientX/clientY
      ripple.style.left = `${e.pageX}px`;
      ripple.style.top = `${e.pageY}px`;

      const cleanupRipple = () => {
        if (ripple.parentNode === container) {
          container.removeChild(ripple);
        }
      };

      ripple.addEventListener("animationend", cleanupRipple, { once: true });
      container.appendChild(ripple);
    };

    el._rippleHandler = _.throttle(createRipple, 50);
    el._mouseenterHandler = mouseenterHandler;
    el._mouseleaveHandler = mouseleaveHandler;

    el.addEventListener("mousemove", el._rippleHandler);
    el.addEventListener("mouseenter", el._mouseenterHandler);
    el.addEventListener("mouseleave", el._mouseleaveHandler);

    el._cleanup = () => {
      if (container.parentNode) {
        document.body.removeChild(container);
      }
    };
  },

  unmounted(el) {
    if (el._rippleHandler) {
      el.removeEventListener("mousemove", el._rippleHandler);
    }
    if (el._mouseenterHandler) {
      el.removeEventListener("mouseenter", el._mouseenterHandler);
    }
    if (el._mouseleaveHandler) {
      el.removeEventListener("mouseleave", el._mouseleaveHandler);
    }
    if (el._cleanup) {
      el._cleanup();
    }
  },
};
