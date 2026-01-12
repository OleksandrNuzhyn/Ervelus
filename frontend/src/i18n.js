import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    home: {
      badge: "5 Free Generations Included • No Credit Card",
      hero_title_1: "Transform Your Photos",
      hero_title_2: "into AI Art",
      hero_subtitle: "Professional styling in one click. Choose from 30+ styles",
      cta_free: "Try for free",

      compare_title: "See the Difference",
      compare_subtitle: "Drag the slider to compare original photo and AI result",
      original: "Original",
      drag_hint: "Drag to compare",

      styles_title: "Unlock Premium Styles",
      styles_subtitle: "Choose your level of access to the AI style library",
      show_styles: "Style List ({count})",
      hide_styles: "Hide List",

      plan_free: "Free Plan",
      plan_amateur: "Amateur",
      plan_journeyman: "Journeyman",
      plan_master: "Master",
      per_month: "/month",
      genes_included: "5 Generations",
      plus_all_from: "+ All styles from the {plan}",
      desc_style_name: "Professional AI styling",
      desc_style_genre: "Full access to 30+ premium styles",
      elders_choice: "Elder's Choice",

      genres_title: "Explore Art Genres",
      genres_subtitle: "From mystical fantasy worlds to sophisticated Victorian balls",
      genre_fantasy: "Aesthetics of mythical realms and legendary creatures",
      genre_punkverse: "Fusion of urban subcultures and technology",
      genre_timetravel: "Visual immersion into different historical epochs",
      genre_world: "Iconic locations and distinct spots across the globe",
      genre_events: "Stylized visuals for festive and large-scale gatherings",
      genre_trending: "Cinematic photography and premium visual aesthetics",

      how_title: "How it Works",
      how_subtitle: "Transform your photos in three simple steps",
      step_1_title: "Upload Your Photo",
      step_1_desc: "Upload a selfie, portrait, or any image from your gallery",
      step_2_title: "Choose Your Style",
      step_2_desc: "Choose from 30+ professional styles",
      step_3_title: "Transform & Download",
      step_3_desc: "Download high-quality art instantly. Ready to share",

      demo_title: "See It in Action",
      demo_subtitle: "Watch the real-time generation process",

      final_title_1: "Ready to create something",
      final_title_2: "extraordinary?",
      final_cta: "Try for free"
    }
  },
  uk: {
    home: {
      badge: "5 генерацій у подарунок • Без водяних знаків",
      hero_title_1: "Перетвори свої фото",
      hero_title_2: "на ШІ-арт",
      hero_subtitle: "Професійна стилізація в один клік. Обирай з 30+ стилів",
      cta_free: "Почати безкоштовно",

      compare_title: "Відчуй різницю",
      compare_subtitle: "Потягни повзунок, щоб порівняти результат",
      original: "Оригінал",
      drag_hint: "Потягни",

      styles_title: "Преміальні стилі",
      styles_subtitle: "Обирай свій рівень доступу до бібліотеки ШІ-стилів",
      show_styles: "Список стилів ({count})",
      hide_styles: "Згорнути список",

      plan_free: "Free Plan",
      plan_amateur: "Amateur",
      plan_journeyman: "Journeyman",
      plan_master: "Master",
      per_month: "/міс",
      genes_included: "5 Генерацій",
      plus_all_from: "+ Всі стилі плану {plan}",
      desc_style_name: "Професійна ШІ-стилізація",
      desc_style_genre: "Повний доступ до 30+ стилів",
      elders_choice: "Вибір Старійшин",

      genres_title: "Жанри",
      genres_subtitle: "Від містичних світів фентезі до витончених вікторіанських балів",
      genre_fantasy: "Естетика міфічних світів та легендарних істот",
      genre_punkverse: "Поєднання урбаністичних субкультур та технологій",
      genre_timetravel: "Візуальне занурення у різні історичні епохи",
      genre_world: "Легендарні локації та знакові місця у різних країнах",
      genre_events: "Стилізовані образи для урочистих та масових подій",
      genre_trending: "Кінематографічна естетика та преміальні візуальні образи",

      how_title: "Як це працює",
      how_subtitle: "Три прості кроки до результату",
      step_1_title: "Завантаж фото",
      step_1_desc: "Селфі, портрет або будь-що з галереї",
      step_2_title: "Обери стиль",
      step_2_desc: "Понад 30 професійних стилів",
      step_3_title: "Отримай результат",
      step_3_desc: "Завантажуй у високій якості та ділись",

      demo_title: "Дивись в дії",
      demo_subtitle: "Процес генерації в реальному часі",

      final_title_1: "Створи свій перший",
      final_title_2: "ШІ-арт",
      final_cta: "Почати безкоштовно"
    }
  }
}

const detectedLocale = Object.keys(messages).find(lang => navigator.language.startsWith(lang))
const fallbackLocale = 'en'

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: detectedLocale || fallbackLocale,
  fallbackLocale,
  messages
})

export default i18n