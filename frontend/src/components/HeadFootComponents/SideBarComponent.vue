<template>
    <div class="relative" ref="profileBar">
        <div class="group">
            <button @click="toggleBar" class="flex items-center gap-2 hover:brightness-125 focus:outline-none">
                <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 400.000000 400.000000"
                    preserveAspectRatio="xMidYMid meet" class="h-10 w-10 text-gray-100 group-hover:text-gray-400" fill="currentColor">
                    <g transform="translate(0.000000,400.000000) scale(0.100000,-0.100000)" stroke="none">
                    <path d="M1963 3555 c-14 -10 -23 -28 -25 -52 l-3 -37 -72 -12 c-232 -39 -440 -241 -522 -506 -14 -48 -30 -76 -53 -97 l-33 -29 2 -104 c2 -136 21 -225 98 -453 44 -129 65 -206 65 -238 0 -38 5 -53 26 -74 l26 -26 -39 -39 c-51 -52 -181 -141 -197 -135 -7 3 -19 26 -26 52 -7 25 -22 52 -34 60 -61 43 -277 -20 -435 -127 -70 -47 -192 -175 -234 -245 -73 -121 -117 -264 -132 -435 -8 -87 4 -121 51 -138 18 -7 24 -15 20 -28 -9 -29 -66 -379 -66 -404 0 -14 10 -34 23 -46 23 -22 29 -22 313 -22 239 0 293 3 311 15 14 10 26 38 38 87 10 40 21 76 24 81 4 4 13 -28 19 -70 21 -131 -80 -118 885 -121 l833 -2 21 22 c15 16 26 51 37 112 9 49 17 90 19 92 2 2 13 -39 26 -91 17 -69 29 -99 44 -110 18 -12 70 -15 307 -15 274 0 287 1 308 20 29 27 28 56 -8 274 -17 98 -30 185 -30 191 0 7 11 16 25 19 14 4 32 18 41 31 15 23 15 37 5 131 -34 297 -161 517 -383 664 -102 67 -233 118 -325 127 -79 7 -105 -8 -123 -71 -7 -26 -16 -48 -20 -51 -10 -6 -130 74 -196 131 l-54 46 30 30 c25 24 30 38 30 76 0 29 21 107 60 221 71 211 100 346 100 471 0 83 -2 93 -25 115 -13 14 -28 25 -33 25 -5 0 -17 30 -27 68 -10 37 -39 108 -64 157 -80 161 -244 300 -410 349 -30 9 -67 16 -83 16 -24 0 -28 4 -28 29 0 36 -35 81 -64 81 -12 0 -31 -7 -43 -15z m264 -261 c92 -44 171 -117 227 -207 45 -74 101 -213 88 -221 -15 -9 -311 -87 -423 -110 l-116 -25 -119 25 c-65 13 -190 43 -277 66 l-158 42 7 31 c13 61 66 172 113 236 81 109 213 193 329 206 l42 6 0 -174 c0 -142 3 -179 16 -197 18 -26 60 -29 86 -5 16 14 18 34 18 193 0 97 2 179 5 182 11 11 91 -13 162 -48z m-518 -625 l284 -71 304 76 c166 42 305 76 308 76 11 0 4 -122 -10 -192 -9 -40 -42 -153 -75 -251 -33 -98 -63 -196 -66 -219 -6 -37 -13 -44 -88 -93 -106 -70 -301 -166 -346 -172 -79 -10 -470 195 -470 247 0 11 -23 86 -51 167 -71 207 -106 340 -115 435 l-7 81 24 -6 c13 -4 152 -39 308 -78z m-29 -850 c96 -56 277 -129 319 -129 42 0 188 57 308 121 l92 49 78 -62 c43 -35 89 -70 103 -80 25 -16 25 -16 5 -32 -158 -126 -432 -245 -570 -248 -135 -3 -435 122 -584 243 l-24 20 23 16 c12 9 57 44 99 79 41 35 77 64 78 64 0 0 33 -19 73 -41z m-542 -209 c37 -111 45 -149 46 -215 0 -71 -3 -86 -29 -134 -16 -29 -45 -66 -65 -83 -93 -77 -268 -128 -445 -128 -141 0 -148 3 -140 54 33 209 130 396 262 501 91 73 248 146 303 142 22 -2 28 -14 68 -137z m1926 100 c227 -95 386 -319 430 -607 l6 -42 -46 -7 c-69 -10 -270 2 -337 20 -172 47 -278 142 -301 268 -9 51 9 152 51 282 19 61 38 115 40 120 9 13 80 -2 157 -34z m-1588 -211 c118 -72 301 -145 437 -174 l27 -5 0 -390 c0 -215 -3 -390 -7 -391 -46 -4 -695 -4 -698 1 -3 5 -33 220 -64 450 l-8 65 40 45 c96 108 127 249 92 419 -21 106 -13 115 60 61 28 -21 83 -57 121 -81z m1246 115 c3 -3 0 -29 -8 -57 -47 -177 -16 -348 81 -456 l38 -41 -36 -257 c-20 -141 -40 -260 -45 -265 -5 -5 -161 -7 -348 -6 l-339 3 0 390 0 389 90 24 c172 45 337 123 475 226 77 57 83 60 92 50z m-1676 -636 c-3 -13 -29 -113 -57 -222 -27 -110 -53 -204 -55 -208 -5 -8 -407 -11 -416 -3 -4 4 41 283 57 351 4 19 14 22 97 28 106 8 264 37 323 60 54 20 58 19 51 -6z m2092 -32 c43 -8 123 -18 180 -21 93 -7 103 -9 107 -29 11 -52 55 -319 55 -336 0 -19 -8 -20 -210 -20 l-209 0 -10 38 c-37 139 -101 398 -101 408 0 10 14 8 56 -6 31 -11 90 -26 132 -34z"/>
                    <path d="M1607 2600 c-38 -30 -33 -88 10 -105 34 -13 344 -75 375 -75 46 0 349 70 376 86 15 10 22 24 22 44 0 29 -29 70 -50 70 -6 0 -85 -16 -177 -36 l-168 -36 -160 32 c-88 17 -169 34 -180 36 -12 3 -32 -4 -48 -16z"/>
                    <path d="M1638 2389 c-16 -9 -18 -26 -18 -132 0 -132 5 -147 50 -147 45 0 50 15 50 147 0 111 -2 123 -19 133 -24 12 -41 12 -63 -1z"/>
                    <path d="M2124 2386 c-17 -13 -19 -29 -22 -173 -3 -177 4 -206 51 -211 54 -6 57 4 57 199 0 166 -1 179 -19 189 -27 14 -44 13 -67 -4z"/>
                    <path d="M2277 2382 c-26 -28 -25 -232 1 -255 24 -22 55 -21 75 1 26 28 25 232 -1 255 -24 22 -55 21 -75 -1z"/>
                    <path d="M1792 2378 c-15 -15 -17 -330 -2 -359 14 -25 61 -25 83 -1 14 16 17 44 17 176 0 89 -4 166 -10 177 -12 22 -68 27 -88 7z"/>
                    <path d="M1966 2324 c-13 -13 -16 -44 -16 -178 0 -174 3 -186 51 -186 54 0 59 16 59 186 0 141 -2 156 -20 174 -24 24 -53 26 -74 4z"/>
                    </g>
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-100 group-hover:text-gray-400 transition-transform duration-200" :class="{'rotate-180': isBarOpen}" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </button>
        </div>
        <transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="transform translate-x-full"
            enter-to-class="transform translate-x-0"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="transform translate-x-0"
            leave-to-class="transform translate-x-full">
            <div v-if="isBarOpen" class="fixed right-0 top-18 h-[calc(100vh-4rem)] py-2 w-80 bg-[#202b32]/30 backdrop-blur-xl z-100 flex flex-col transform-gpu">
                <div class="px-3 py-4 text-sm text-gray-400 flex items-center justify-between">
                    <span>COINS: {{ credits }}</span>
                    <img src="@/assets/svg/coin.svg" class="h-9 w-9 mr-1" />
                </div>
                <router-link to="/profile" class="px-4 py-4 text-sm text-gray-400 hover:text-white flex items-center justify-between" @click="closeBar">
                    <span>Profile</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </router-link>
                <router-link to="/pricing" class="px-4 py-4 text-sm text-gray-400 hover:text-white flex items-center justify-between" @click="closeBar">
                    <span>Pricing</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </router-link>
                <router-link to="/contact-us" class="px-4 py-4 text-sm text-gray-400 hover:text-white flex items-center justify-between" @click="closeBar">
                    <span>Contact us</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"/>
                    </svg>
                </router-link>
                <div class="mt-auto flex flex-col overflow-hidden">
                    <div class="flex-grow flex flex-col justify-end overflow-hidden" style="-webkit-mask-image: linear-gradient(to top, black 85%, transparent 100%); mask-image: linear-gradient(to top, black 85%, transparent 100%);">
                        <img src="@/assets/svg/sidebar.webp" class="w-full" />
                    </div>
                    <button @click="onLogout" class="w-full text-left px-4 py-4 text-sm bg-black/20 text-gray-400 hover:text-white flex items-center justify-between flex-shrink-0">
                        <span>Sign out</span>
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20V9.75a5 5 0 00-10 0V20M2 20h20"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 12h8m0 0l-3-3m3 3l-3 3"></path></svg>
                    </button>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, toRefs } from 'vue';

const props = defineProps({
    credits: {
        type: Number,
        default: 0,
    },
});

const emit = defineEmits(['open-change', 'logout']);

const { credits } = toRefs(props);

const isBarOpen = ref(false);
const profileBar = ref(null);

const toggleBar = () => {
    isBarOpen.value = !isBarOpen.value;
};

const closeBar = () => {
    if (!isBarOpen.value) {
        return;
    }

    isBarOpen.value = false;
};

const handleClickOutside = (event) => {
    if (profileBar.value && !profileBar.value.contains(event.target)) {
        closeBar();
    }
};

onMounted(() => {
    document.addEventListener('mousedown', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('mousedown', handleClickOutside);
});

watch(isBarOpen, (newValue) => {
    emit('open-change', newValue);
});

const onLogout = () => {
    closeBar();
    emit('logout');
};

defineExpose({
    closeBar,
});
</script>