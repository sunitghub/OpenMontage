# Diety: Maa Tara
# Title: Maa Tara Helps With Court Case

## Render Commands

```bash
# Single scene (EQ baked in, random zoom per card)
render-scene --scene 1 --narration Scene-1.mp3 --preview   # fast 720p draft

# All scenes — pre-checks each scene for Scene-N.mp3, skips missing, concats to Full-test.mp4
render-scene --all
render-scene --all --vintage --preview

# Critic / pacing audit (no render)
render-scene --critic

 Workflow:
  1. Cursor anywhere inside a scene (e.g. Scene-3)
  2. C-c o P → auto-reads ### Script English, generates 3 prompts
  3. C-u 7 C-c o P → generates 7 prompts
  4. Progress streams in the side panel → on completion, prompts are numbered and inserted
  directly under #### Images in the file, side panel shows "Done — prompts inserted into file"

  Two commands, two use cases:
  - C-c o p — manual selection → side buffer (for experimenting/tweaking)
  - C-c o P — scene-aware → inserts directly into the markdown file
  (global-set-key (kbd "C-c o i") #'om/insert-at-marker)
(global-set-key (kbd "C-c o s") #'om/goto-scene)
(global-set-key (kbd "C-c o n") #'om/new-scene)
(global-set-key (kbd "C-c o p") #'om/image-prompts)
(global-set-key (kbd "C-c o P") #'om/scene-image-prompts)
(global-set-key (kbd "C-c o t") #'om/translate)
```

## Character Bible

Generate these reference images first. All scene prompts should visually match these anchors.

> **GPT-4o note:** No reference image needed for Character Bible generations — these ARE the references.

### Maa Tara

   **Ref:** Upload `Tara-Maa-3.jpg`

		painterly AI devotional illustration, Hindustani folk-story art style, full-figure character bible portrait of Maa Tara Devi standing upright in slight tribhanga posture, deep blue radiant complexion, four arms — upper-right hand holding a  curved silver khadga sword, upper-left hand holding a blue utpala lotus, lower-right hand holding kartri scissors, lower-left hand holding a dark kapala skull cup — long unbound black hair cascading behind her, three eyes open and calm with the third eye on the forehead, large ornate golden crown with tiered crest, full golden jewelry — necklace, armlets, armlets, anklets — flowing red and gold sari with ornate border draped naturally, standing on the chest of a supine Shiva figure at the base of the frame, twin fires burning on both left and right behind her, billowing golden-orange clouds in the upper background, expression fierce and powerful yet unmistakably benevolent and maternal, divine presence not demonic, warm golden ambient light surrounding her form, centered full-figure composition with subject filling the frame, character reference illustration — this face complexion ornaments and clothing must remain consistent across all future scenes, polished folk illustration, no other figures beside Shiva at base, no text, no watermark
		
#### Maa Tara Signifies

**The Four Arms**

	- **Khadga (Curved Sword) — Upper Right:** The sword of divine knowledge that cuts through ignorance, ego, and the illusions of maya. She severs the bonds of karma, clearing the path to liberation.

	- **Utpala (Blue Lotus) — Upper Left:** Spiritual wisdom and elevated consciousness rising pure from the muddy waters of samsara. The blue lotus connects to Vishuddha — the throat chakra — affirming Tara as *Shabda Brahman*, the divine in the form of sound, ruler of speech and mantra.

	- **Kartri (Scissors) — Lower Right:** Cuts the thread of karmic attachment and the cycle of rebirth. What binds the soul to suffering, she severs.

	- **Kapala (Skull Cup) — Lower Left:** Transcendence of ego and mortality. She holds death itself as a vessel — consuming darkness and transforming it into liberation. The empty skull is the egoless state of moksha.

**Deeper Symbolism**

	- **Blue Complexion** — The infinite void, the unmanifest cosmic space from which all creation arises and returns.
	- **Three Eyes** — Omniscience: right eye is the Sun, left is the Moon, forehead eye is Fire. She sees past, present, and future simultaneously.
	- **Standing on Shiva** — Shakti as dynamic creative energy activating inert Shiva (pure Consciousness). She does not defeat him — she animates him. He is the ground of being; she is the force that moves it.
	- **Twin Fires** — The fire of purification and transformation through which devotees pass to reach her grace.

---


### Sadhak-A (Ravi)

   **Ref:** Upload `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of a young Indian man in his late twenties, medium-warm wheatish complexion, sharp and defined facial features, dark brown hair naturally voluminous and wavy with a tousled quality, short neatly trimmed beard, warm brown expressive eyes, calm and earnest expression with a slight upward gaze, wearing a white Mandarin-collar kurta, three-quarter upper-body composition facing slightly left, warm golden ambient light, soft ochre-toned background, no text, no watermark — this face hair complexion and expression must remain consistent across all future scenes


### Sadhak-B (Ravi — Sadhana attire)

   **Ref:** Upload `Sadhak-B.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of the same young Indian man as Sadhak-A — identical face, medium-warm wheatish complexion, dark brown hair naturally voluminous and wavy with a tousled quality, short neatly trimmed beard, warm brown expressive eyes — dressed in sadhana attire: rose-pink dhoti wrapped traditionally around the lower body, a soft rose-pink shawl draped loosely open over both shoulders leaving the chest bare in the traditional manner, holding a dark brown rudraksha mala in the right hand raised to chest height with fingers resting on the beads, slight upward gaze, expression serene and inwardly focused, warm golden ochre background, soft warm ambient light, centered three-quarter upper-body composition, no text, no watermark — this face and sadhana attire must remain consistent across all scenes depicting the sadhana ritual


### Tara Yantra

   **Ref:** Upload `Yantra-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible reference for the Tara Yantra — recreate this sacred geometric diagram exactly as shown in the uploaded image: square outer boundary with four gate-like projections, eight-petalled lotus at the center, a circle enclosing an upward-pointing triangle at the heart — rendered in glowing rose-gold lines on a deep dark background, soft divine radiance emanating from the diagram, precise sacred geometry, no figures, no additional text, no watermark — this yantra layout must remain structurally consistent across all scenes where it appears


### Sadhana Room

   **Ref:** Upload `Room-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, interior of an empty room in a modern 2020s Indian apartment, all four smooth freshly painted walls and ceiling a soft rose-pink, clean ceramic floor tiles, modern flush LED ceiling light fitting casting warm even light, glass-paned window with simple white curtains, plain skirting boards, no furniture, no figures, no clutter — generate this as the room reference; this interior must remain visually consistent across all sadhana preparation scenes


### Guru

   **Ref:** Upload `Guru-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of an older Indian spiritual master in his fifties, powerfully muscular bare chest, long dark wavy voluminous hair falling past the shoulders, clean-shaven face with a large thick handlebar mustache with prominent upward-rolled ends — no beard, a bold red tilak on the forehead, large heavy rudraksha mala hanging around the neck, rudraksha bracelet on the wrist, saffron-orange cloth draped around the lower body and loosely over one shoulder, seated cross-legged in an authoritative posture, expression intense and commanding yet deeply wise, ancient stone temple wall in the background, dramatic dhuni fire burning at his feet casting strong upward amber light, skull and brass ritual vessels at the base, warm amber and ochre tones, centered full-figure composition, no text, no watermark — this face build mustache and attire must remain consistent across all scenes featuring the Guru


## Scene-1:

### Script Hindi 

	Namaste Doston. Blissful chants main aapka swagat hai. Aaj ke, is episode  main, hum Ravi ke, Tara Sadhan ke anubhav, ke baren main sunege, jo usne apne Guru ke kehne par sampaan kari. Guru ne Ravi se, shukla paks ke kisi bhi, Budhwar se raat 9 se 3 baje ke beech main, sadahan ko, sampan karne ko, kaha tha.
	
	Maa Tara ko char bhujaon ke saath darshaya gaya hai, jinmein se pratyek unki divya shakti ka prateek hai: agyan aur ahankaar ko kaatne ke liye ek talwar; unnat chetna aur gyan ke liye ek neela kamal; karm aur punarjanm ke bandhanon ko kaatne ke liye canchi; aur ek kapal-patra — jahan andhkar ka bhakshan hota hai aur wah mukti mein rupantarit ho jata hai। ve ugra bhi hain aur mamtamayi bhi — wah divya shakti jo aatma ko mukt karti hai।
	
	Guru ka aadesh thaa, ki Maa Tara ko, gulabi rang priya thaa, isiliye Ravi ko, Sadhana ki sabhi samagriyaan, isi rang maen tayaar karni thi. Ravi ne, apne ghar ka ek kamra, saaf kiya, aur uski diwalen aur chath par gulabi rang karvaya. Phir, usne farsh par, lagbhag chhah inch uncha, ek lakdi ka takhta rakha, use ek gulabi kapde se dhaka, aur uske samne ek gulabi aasan rakh diya. Usne aasan ko, is tarah bichhaya, ki jab woh us par baithta, to uska muh uttar disha ki aur hoga. 
	
	Iske bad, usne lagbhag 2 kilogram chawalon ko gulabi rang diya aur unse bajot par, aath pankhudiyon wala, ek kamal ka phool banaya. Phir usne, uske theek beech mein, mitti ka ek mota deepak rakha. Deepak shuddh ghee se bhara hua tha, aur uski baati gulabi rang ki rui se bani thi.
	
	
### Script English

	Namaste, friends. Welcome to Blissful Chants. In today's episode, we will hear about Ravi's experience with the Tara Sadhana, which he performed at the behest of his Guru. The Guru had instructed Ravi to perform this Sadhana on any Wednesday during the *Shukla Paksha* (waxing phase of the moon), between the hours of 9:00 PM and 3:00 AM.

	Maa Tara is depicted with four arms, each a symbol of her divine power: a sword to cut through ignorance and ego, a blue lotus for elevated consciousness and wisdom, scissors to sever the bonds of karma and rebirth, and a skull cup — where darkness is consumed and transformed into liberation. She is fierce and maternal both — the divine force that frees the soul.

	The Guru had ordered that Mother Tara loved the color pink, hence Ravi had to prepare all the materials for Sadhana in this color. Ravi cleaned up a room in his house and got the ceilings and walls painted pink. Then, he placed a wooden plank—approximately six inches high—on the floor, covered it with a pink cloth, and placed a pink cushion in front of it. The rug was positioned so that when Ravi sat on it, he faced north.
	
	Next, he colored about 2 kg of rice pink and made an eight-petalled lotus flower with it on the board. He then placed a thick earthenware lamp in its center. The lamp was filled with pure ghee, and the wick was made from pink-dyed cotton wool.
		
	

### Artifacts


#### Images

**1. Maa Tara appears — divine opening**
> Refs: `Tara-Maa-3.jpg` + `Room-Ref.jpg` + `Sadhak-B.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, full interior view of the modern rose-pink room — Maa Tara hovering in the center of the room, slightly zoomed out to show the full room around her, her deep blue radiant form luminous and divine, four arms — upper-right holding curved silver khadga, upper-left holding blue lotus, lower-right kartri scissors, lower-left kapala skull cup — a large brilliant golden halo radiating behind her head, right palm turned outward in abhaya mudra with a soft golden ray of divine light streaming gently from her palm downward — in the foreground at the base of the image the Sadhak kneeling and looking upward with face lifted toward Maa Tara, eyes wide with awe and devotion, pink sadhana attire visible, rudraksha mala in hand, overwhelmed with reverence — Maa Tara gazing downward directly at him with a compassionate and powerful expression, eyes meeting his, a moment of divine connection — pink walls and window with white curtains visible on both sides, divine golden-white radiance flooding the room, ceramic tiled floor reflecting her glow, awe-inspiring and captivating, no text no watermark

**2. The Guru gives instructions to Ravi**
> Refs: `Guru-Ref.jpg` + `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, two figures in a dimly lit traditional Indian setting — on the left the Guru seated cross-legged, bare-chested, saffron cloth draped around him, large rudraksha mala, red tilak on forehead, large thick handlebar mustache with upward-rolled ends and no beard, one hand raised in a gesture of instruction, expression authoritative and wise — on the right the Sadhak seated before him in namaskar posture with palms joined and head slightly bowed in respectful attention, wearing a simple white kurta — a small sacred dhuni fire burning low between them casting warm amber light on both faces, dark moody background with deep shadows, intimate guru-shishya atmosphere, no text no watermark

**3. Ravi surveys the empty room**
> Refs: `Room-Ref.jpg` + `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, young Indian man standing in the doorway of a bare empty room in a modern 2020s Indian apartment, sleeves rolled up, thoughtful and determined expression, smooth freshly painted off-white walls, ceramic tiled floor, modern flush ceiling light fitting casting clean warm light, contemporary door frame with clean finish, glass-paned window with simple curtains, two rose-pink paint buckets near the door with fresh paint dripping down their outer edges, paint stirrer resting in one of them, lids leaning against the wall — sense of quiet resolve, no text no watermark

**4. The room transformed — walls painted pink**
> Refs: `Room-Ref.jpg` + `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, the Sadhak standing at the center of a freshly painted room in a modern 2020s Indian apartment, all four smooth walls and ceiling now a soft rose-pink, a paint roller resting against the wall beside him, hands slightly paint-stained, he surveys his work with calm satisfaction, ceramic tiled floor, modern flush ceiling light, contemporary glass-paned window, empty floor still to be set up, no text no watermark

**5. Placing the wooden plank**
> Refs: `Room-Ref.jpg` + `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, the Sadhak kneeling on the ceramic tiled floor of a modern Indian apartment room, carefully lowering a flat wooden plank approximately six inches high onto the floor, focused and reverent expression, smooth rose-pink painted walls visible in background, modern flush ceiling light, contemporary interior, no text no watermark

**6. The altar cloth and cushion — detail shot**
> Refs: `Room-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, close view of a low wooden board draped in a smooth rose-pink cloth, folds falling neatly at the edges, a thick pink velvet cushion placed on the ceramic tiled floor directly in front of the board, smooth rose-pink painted walls visible at the edges, modern glass-paned window with soft evening light from outside, warm soft glow, devotional stillness, no figures, no text no watermark

**7. Sadhak arranging the rice lotus**
> Refs: `Room-Ref.jpg` + `Sadhak-A.jpg` + `Yantra-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, the Sadhak kneeling over the pink-cloth-covered board, hands carefully placing pink-dyed rice grains forming an eight-petalled lotus matching the Tara Yantra layout — eight petals with a circle and upward triangle at the center, his face close to the board with deep concentration, the nearly-complete pattern visible beneath his hands, warm light from a modern flush ceiling fitting overhead, smooth rose-pink painted walls framing the scene, ceramic tiled floor, contemporary Indian apartment interior, no text no watermark

**8. The Tara Yantra — beauty shot**
> Refs: `Yantra-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, close-up beauty shot of a sacred Hindu yantra (ref: Yantra-Ref.jpg) rendered in glowing rose-gold lines on a deep dark background — square outer boundary with four gate-like projections on each side, an eight-petalled lotus flower at the center, inside the lotus a circle enclosing an upward-pointing triangle, the entire geometric diagram emanating a soft golden divine radiance as if lit from within, intricate precise linework, sacred geometric beauty, no figures, no text no watermark

**9. The eight-petalled rice lotus — detail shot**
> Refs: `Room-Ref.jpg` + `Yantra-Ref.jpg`

	Hindustani folk-story art style, painterly illustration with visible brush strokes and warm paint texture — NOT photorealistic, NOT 3D render, wide landscape composition, bird's-eye close-up of a perfectly formed eight-petalled lotus made entirely from pink-dyed rice grains arranged on a rose-pink cloth, exactly eight petals symmetrical and precise matching the Tara Yantra layout, a circular empty space at the very center with a subtle triangle outline — empty and awaiting the lamp, soft warm overhead light catching the texture of each grain, sacred geometric beauty, no lamps, no bowls, no props, no figures, no text, no watermark

**10. The earthenware lamp — detail shot**
> Refs: `Room-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, close-up of a thick hand-thrown earthenware deepak placed at the center of the rice lotus, filled with pure golden ghee, a slender pink-dyed cotton wick rising from its center, a single flame just lit — golden and steady, warm glow reflecting off the surrounding pink rice petals, devotional and sacred atmosphere, no figures, no text no watermark

**11. The completed sadhana room at night**
> Refs: `Room-Ref.jpg` + `Sadhak-B.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, full interior view of the sadhana room at night in a modern Indian apartment, all four smooth walls and ceiling rose-pink, ceramic tiled floor, contemporary glass-paned window dark with night outside, wooden board on the floor covered in pink cloth with the eight-petalled rice lotus and lit earthenware lamp glowing at its center, the Sadhak seated cross-legged on the pink cushion directly before the board facing north, hands resting on knees in meditation posture, eyes closed, warm golden lamplight illuminating his face and the room, overhead light switched off — only the deepak flame lighting the space, deep devotional stillness, no other figures, no text no watermark



## Scene-2:

### Script Hindi


### Script English

	
#### Artifacts

##### Images


	
	
	







## Description
	
	  
	🙏 Jai Maa Tara 🙏

  ---
  
	Disclaimer: This story is a personal spiritual experience, narrated as shared by the devotee. It is presented for devotional and inspirational purposes only. Spiritual experiences are personal and results vary. Viewers are encouraged to seek guidance from a qualified Guru before undertaking any sadhana or spiritual 
	
	#MaaTara #TrueStory #Sadhana #DevotionalStory #Tara #Kali
