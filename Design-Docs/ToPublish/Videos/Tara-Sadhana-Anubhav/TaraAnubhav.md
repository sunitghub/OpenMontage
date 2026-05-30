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

	
	painterly AI devotional illustration, Hindustani folk-story art style, full-figure character bible portrait of Maa Tara Devi standing upright in slight tribhanga
	posture, deep blue radiant complexion, four arms — upper-right hand holding a  curved silver khadga sword, upper-left hand holding a blue utpala lotus, lower-right hand holding kartri scissors, lower-left hand holding a dark kapala skull cup — long unbound black hair cascading behind her, three eyes open and calm with the third eye on the forehead, large ornate golden crown with tiered crest, full golden jewelry — necklace, armlets, armlets, anklets — flowing red and gold sari with ornate border draped naturally, standing on the chest of a supine Shiva figure at the base of the frame, twin fires burning on both left and right behind her, billowing golden-orange clouds in the upper background, expression fierce and powerful yet unmistakably benevolent and maternal, divine presence not demonic, warm golden ambient light surrounding her form, centered full-figure composition with subject filling the frame, character reference illustration — this face complexion ornaments and clothing must remain consistent across all future scenes, polished folk illustration, no other figures beside Shiva at base, no text, no watermark


### Sadhak-A (Ravi)

   **Ref:** Upload `Sadhak-A.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of a young Indian man in his late twenties, medium-warm wheatish complexion, sharp and defined facial features, dark brown hair naturally voluminous and wavy with a tousled quality, short neatly trimmed beard, warm brown expressive eyes, calm and earnest expression with a slight upward gaze, wearing a white Mandarin-collar kurta, three-quarter upper-body composition facing slightly left, warm golden ambient light, soft ochre-toned background, no text, no watermark — this face hair complexion and expression must remain consistent across all future scenes


### Sadhak-B (Ravi — Sadhana attire)

   **Ref:** Upload `Sadhak-B.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of the same young Indian man as Sadhak-A — identical face, medium-warm wheatish complexion, dark brown hair naturally voluminous and wavy with a tousled quality, short neatly trimmed beard, warm brown expressive eyes — dressed in sadhana attire: rose-pink dhoti wrapped traditionally around the lower body, a soft rose-pink shawl draped loosely open over both shoulders leaving the chest bare in the traditional manner, holding a dark brown rudraksha mala in the right hand raised to chest height with fingers resting on the beads, slight upward gaze, expression serene and inwardly focused, warm golden ochre background, soft warm ambient light, centered three-quarter upper-body composition, no text, no watermark — this face and sadhana attire must remain consistent across all scenes depicting the sadhana ritual


### Guru

   **Ref:** Upload `Guru-Ref.jpg`

	painterly AI devotional illustration, Hindustani folk-story art style, character bible portrait of an older Indian spiritual master in his fifties, powerfully built bare chest, long dark hair falling to the shoulders, clean-shaven face with a large thick handlebar mustache with upward-rolled ends — no beard, a bold red tilak on the forehead, large rudraksha mala hanging around the neck, saffron-orange cloth draped around the lower body and loosely over one shoulder, seated cross-legged in an authoritative posture, expression intense and commanding yet deeply wise, dark warm background with a suggestion of a sacred dhuni fire at the base, amber and ochre tones, centered three-quarter upper-body composition, no text, no watermark — this face build mustache and attire must remain consistent across all scenes featuring the Guru


## Scene-1:

### Script Hindi 

	Namaste Doston. Blissful chants main aapka swagat hai. Aaj ke, is episode  main, hum Ravi ke, Tara Sadhan ke anubhav, ke baren main sunege, jo usne apne Guru ke kehne par sampaan kari. Guru ne Ravi se, shukla paks ke kisi bhi, Budhwar se raat 9 se 3 baje ke beech main, sadahan ko, sampan karne ko, kaha tha.
	
	Guru ka aadesh thaa, ki Maa Tara ko, gulabi rang priya thaa, isiliye Ravi ko, Sadhana ki sabhi samagriyaan, isi rang maen tayaar karni thi. Ravi ne, apne ghar ka ek kamra, saaf kiya, aur uski diwalen aur chath par gulabi rang karvaya. Phir, usne farsh par, lagbhag chhah inch uncha, ek lakdi ka takhta rakha, use ek gulabi kapde se dhaka, aur uske samne ek gulabi aasan rakh diya. Usne aasan ko, is tarah bichhaya, ki jab woh us par baithta, to uska muh uttar disha ki aur hoga. 
	
	Iske bad, usne lagbhag 2 kilogram chawalon ko gulabi rang diya aur unse bajot par, aath pankhudiyon wala, ek kamal ka phool banaya. Phir usne, uske theek beech mein, mitti ka ek mota deepak rakha. Deepak shuddh ghee se bhara hua tha, aur uski baati gulabi rang ki rui se bani thi.
	
	
### Script English

	Namaste, friends. Welcome to Blissful Chants. In today's episode, we will hear about Ravi's experience with the Tara Sadhana, which he performed at the behest of his Guru. The Guru had instructed Ravi to perform this Sadhana on any Wednesday during the *Shukla Paksha* (waxing phase of the moon), between the hours of 9:00 PM and 3:00 AM.
	
	The Guru had ordered that Mother Tara loved the color pink, hence Ravi had to prepare all the materials for Sadhana in this color. Ravi cleaned up a room in his house and got the ceilings and walls painted pink. Then, he placed a wooden plank—approximately six inches high—on the floor, covered it with a pink cloth, and placed a pink cushion in front of it. The rug was positioned so that when Ravi sat on it, he faced north.
	
	Next, he colored about 2 kg of rice pink and made an eight-petalled lotus flower with it on the board. He then placed a thick earthenware lamp in its center. The lamp was filled with pure ghee, and the wick was made from pink-dyed cotton wool.
		
	
### Artifacts


#### Images

> **GPT-4o note:** Upload both `Tara-Maa-3.jpg` and `Sadhak-A.jpg` for all prompts that include Sadhak-A. For detail/environment shots, upload `Tara-Maa-3.jpg` only to maintain style anchor. For Guru scenes upload `Guru-Ref.jpg` + `Sadhak-A.jpg`.

**1. The Guru gives instructions to Ravi**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, two figures in a dimly lit traditional Indian setting — on the left the Guru (ref: Guru-Ref.jpg) seated cross-legged, bare-chested, saffron cloth draped around him, large rudraksha mala, red tilak on forehead, large thick handlebar mustache with upward-rolled ends and no beard, one hand raised in a gesture of instruction, expression authoritative and wise — on the right Sadhak-A (ref: Sadhak-A.jpg) seated before him in namaskar posture with palms joined and head slightly bowed in respectful attention, wearing a simple white kurta — a small sacred dhuni fire burning low between them casting warm amber light on both faces, dark moody background with deep shadows, intimate guru-shishya atmosphere, no text no watermark

**2. Ravi surveys the room before preparation**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, young Indian man (Sadhak-A — ref: Sadhak-A.jpg) standing in the doorway of a plain bare room in a modest Indian home, sleeves rolled up, thoughtful and determined expression, warm late-evening interior light streaming from a single bulb, plain whitewashed walls, empty floor, sense of quiet resolve before the work begins, no text no watermark

**3. The room transformed — walls painted pink**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, Sadhak-A (ref: Sadhak-A.jpg) standing at the center of a freshly painted room, all four walls and ceiling a soft rose-pink, a paint roller resting against the wall beside him, hands slightly paint-stained, he surveys his work with calm satisfaction, late-night interior warm light, empty floor still to be set up, no text no watermark

**4. Placing the wooden plank**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, Sadhak-A (ref: Sadhak-A.jpg) kneeling on the pink-walled room's floor, carefully lowering a flat wooden plank approximately six inches high onto the floor, focused and reverent expression, soft warm lamplight, the pink walls visible in background, humble Indian home interior, no text no watermark

**5. The altar cloth and cushion — detail shot**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, close view of a low wooden board draped in a smooth rose-pink cloth, folds falling neatly at the edges, a thick pink velvet cushion placed on the floor directly in front of the board, compass direction north implied by slight window light, warm soft glow, devotional stillness, no figures, no text no watermark

**6. Sadhak-A arranging the rice lotus**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, Sadhak-A (ref: Sadhak-A.jpg) kneeling over the pink-cloth-covered board, hands carefully placing pink-dyed rice grains in the form of an eight-petalled lotus, his face close to the board with deep concentration, the nearly-complete lotus pattern visible beneath his hands, warm golden light from a single bulb overhead, pink walls framing the scene, no text no watermark

**7. The eight-petalled lotus — detail shot**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, bird's-eye close-up of a perfectly formed eight-petalled lotus made entirely from pink-dyed rice grains arranged on a rose-pink cloth, petals symmetrical and precise, a circular empty space at the very center awaiting the lamp, soft warm overhead light catching the texture of each grain, sacred geometric beauty, no figures, no text no watermark

**8. The earthenware lamp — detail shot**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, close-up of a thick hand-thrown earthenware deepak placed at the center of the rice lotus, filled with pure golden ghee, a slender pink-dyed cotton wick rising from its center, a single flame just lit — golden and steady, warm glow reflecting off the surrounding pink rice petals, devotional and sacred atmosphere, no figures, no text no watermark

**9. The completed sadhana room at night**

	painterly AI devotional illustration, Hindustani folk-story art style, wide landscape composition, full interior view of the sadhana room at night, all four walls and ceiling rose-pink, wooden board on the floor covered in pink cloth with the eight-petalled rice lotus and lit earthenware lamp glowing at its center, Sadhak-A (ref: Sadhak-A.jpg) seated cross-legged on the pink cushion directly before the board facing north, hands resting on knees in meditation posture, eyes closed, warm golden lamplight illuminating his face and the room, deep devotional stillness, no other figures, no text no watermark



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
