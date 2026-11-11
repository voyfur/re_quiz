# Race Expert Controlled Vocabularies & Signal Taxonomy

This document lists the normative controlled terms accepted by the Race Expert Quiz Matching Engine (`draft_matcher.py` and `client_matcher.js`). Any new kit onboarded into the system must use terms strictly from these vocabularies.

---

## 1. Goal Groups (Primary Buyer Needs)

Every product kit must map to one or more primary goal families. In the quiz, these form Step 1:

| Goal Code | Label (UK) | Label (RU) | Core Purpose |
|---|---|---|---|
| `running` | Біг і підготовка до стартів | Бег и старты | Road running, trail running, marathons, sprint race prep |
| `training` | Тренування та сила | Тренировки и сила | Gym, strength, muscle hypertrophy, crossfit, powerlifting |
| `hydration` | Гідратація та електроліти | Гидратация | Isotonics, electrolytes, hypo-osmolal hydration fluids |
| `food` | Перекуси та харчування | Перекусы и питание | Energy bars, carb snacks, energy gels, race nutrition |
| `recovery` | Відновлення та сон | Восстановление и отдых | Post-workout muscle recovery, sleep, joint health, magnesium |
| `outdoors` | Походи й активний відпочинок | Походы и активный отдых | Hiking, camping, trekking, long outdoor expeditions |
| `gear` | Одяг та аксесуари | Одежда и аксессуары | Socks, caps, race number belts, bottles, shakers |
| `daily` | Щоденна підтримка та вітаміни | Ежедневное использование | Daily vitamins, Omega-3, D3, vitality, focus complexes |
| `gift` | Подарунковий набір | Подарок | Curated branded gift sets, apparel combos, club bundles |

---

## 2. Activity Groups (`activity_groups`)

Specific sports or disciplines that the kit supports:

* `running` — шосе, трейл, легка атлетика
* `cycling` — шосейний, гравійний або гірський велоспорт
* `hiking` — трекінг, походи, кемпінг
* `strength_training` — бодібілдинг, робота з вагами, пауерліфтинг
* `functional_training` — кросфіт, кругові тренування, HIIT
* `swimming` — плавання у басейні та відкритій воді
* `mind_body_mobility` — йога, пілатес, стретчинг
* `walking` — скандинавська та оздоровча ходьба
* `general_fitness` — загальна фізична підготовка
* `other` — спеціальний вибір для інших дисциплін

---

## 3. Component Classes (`component_classes`)

Categories of products present in the kit composition:

* `protein_carbohydrate_food` — протеїнові та вуглеводні батончики, печиво, снеки
* `supplements_vitamins_minerals` — вітаміни (D3, C, B-complex), мінерали (Mg, Zn), омега-3
* `creatine_preworkout` — креатин моногідрат, передтренувальні шот-комплекси, бета-аланін
* `hydration_items` — електролітні стики, таблетки, ізотонічний порошок
* `sports_accessories` — пляшки, шейкери, пояси для номерів, тримачі гелів
* `apparel_footwear` — бігові та трекінгові шкарпетки, кепки, бандани
* `dehydrated_meal` — сублімовані туристичні страви швидкого приготування
* `club_membership` — клубний абонемент Race Expert Club

---

## 4. Product Forms (`product_forms`)

Physical delivery format of the products:

* `gel` — енергетичні гелі у тюбиках або пакетиках
* `bars` — батончики (протеїнові, енергетичні, вівсяні)
* `liquid` — рідкі шоти, концентрати, ампули
* `powder` — сухий порошок у банках чи мішках (креатин, протеїн, ізотонік)
* `sticks` — порційні саше або стики з порошком
* `capsules` — стандартні капсули
* `softgels` — м'які желатинові капсули (вітамін D3, Омега-3)
* `tablets` — пресовані таблетки
* `apparel` — шкарпетки, кепки, текстильні вироби
* `food_or_meal` — порційна готова їжа або снеки

---

## 5. Use Contexts (`use_contexts`)

### Scenarios (`use_scenario`):
* `event_preparation` — підготовка до забігу, марафону чи змагань
* `training` — тренувальні цикли, зал, щотижневі сесії
* `everyday` — на кожен день, для робочого дня чи відпочинку

### Timing (`use_timing`):
* `before_or_after_training` — до або після тренування
* `during_training` — безпосередньо під час навантаження (на дистанції)
* `daily_use` — ранковий або денний щоденний прийом
* `evening_or_bedtime` — ввечері або перед сном (магній, релакс)

### Place (`use_place`):
* `hiking_or_camping` — на природі, у поході
* `travel_or_road` — у подорожі, за кермом
* `work_or_study` — в офісі, під час розумової праці

---

## 6. Race Formats (`race_formats`)

* `half_marathon` — напівмарафон (21.1 км)
* `marathon` — класичний марафон (42.2 км)
* `race_or_event_preparation` — короткі забіги або клубні старти (5–10 км)
* `ultra_or_long_distance` — ультрамарафони, 50+ км, добові старти, триатлон Ironman

---

## 7. Weather & Season (`weather_signals`)

* `cold_weather` — термошкарпетки, теплий текстиль, зимовий тренінг
* `hot_weather` / `summer` — літні кепки, підвищена гідратація, шкарпетки з тонкою сіткою

---

## 8. Sizing (`size_values`)

Applicable when `size_sensitive: true`:
```json
[
  {"type": "shoe_or_sock_size", "value": "35-37"},
  {"type": "shoe_or_sock_size", "value": "38-40"},
  {"type": "shoe_or_sock_size", "value": "40-42"},
  {"type": "shoe_or_sock_size", "value": "43-45"},
  {"type": "shoe_or_sock_size", "value": "46-48"}
]
```
If size is unknown or clothing without numerical shoe sizes, do not guess; flag `size_sensitive: false`.
