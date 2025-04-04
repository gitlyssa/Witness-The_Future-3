﻿define l = Character(name=("Lex Machina"), image="lex", dynamic=False)
define s = Character(name=("Steve"), image="steve", dynamic=False)
define j = Character(name=("Judge"), image="navya", dynamic=False)

default player_fname = ""
default player_lname = ""
default player_prefix = ""
default reminder_pressed = False
default answered_first_question = False
default switch_cases = False
default tutorial_skipped = False  # Fixed with "default"
default context_history = []
default unintelligible_count = 0
default mentioned_truths = set()
default qualification_score = 0
default voir_dire_question_count = 0 
default first_question_generated = False
default voir_dire_retries = 0
default ai_question = ""
default user_answer = ""
$ persistent.case_choice = None
$ persistent.specialty = None


label start:
    scene bg spec
    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Case_A_Anthropology_1", "Case_A_Anthropology_2", "Case_A_Biology_1", "Case_A_Biology_2", "Case_B_Psychology_1", "Case_A_Toxicology_1", "Case_A_Toxicology_2", "Case_A_Psychology_1", "Case_A_Psychology_2", "Case_A_Identification_1", "Case_A_Identification_2", "Case_B_Anthropology_1", "Case_B_Anthropology_2", "Case_B_Biology_1", "Case_B_Biology_2", "Case_B_Chemistry_1", "Case_B_Chemistry_2", "Case_B_Psychology_1", "Case_B_Psychology_2", "Case_B_Identification_1", "Case_B_Identification_2", "Handprint", "Gin", "Splatter", "Footprint"] # holds names for inspect pop-up text
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 105 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 300 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_padding = 120 / 2 # sets padding size between toolbox slots
    $toolbox_first_slot_x = 105 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 300 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 120 / 2 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    # show screen inventory 

label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        #addToInventory(["fingerprint", "handprint", "gin", "splatter", "footprint"])

        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            # if item == "lid":
            #     environment_sprites[-1].width = 300 / 2
            #     environment_sprites[-1].height = 231 / 2
            #     environment_sprites[-1].x = 1000
            #     environment_sprites[-1].y = 500
        
    # scene scene-1-bg at half_size - sets background image
    
    show steve normal2
    s "Welcome to the courtroom. My name is Steve, and I'll be guiding you through your preparation before you deliver expert testimony!"
    s "Would you like me to go through the tutorial? Or should we get straight to selecting your preferences?"
    hide steve normal2

    menu:
        "Would you like to do the tutorial, or skip to selecting your preferences?"
        "Let's do the tutorial first":
            $ tutorial_skipped = False
            jump tutorial_start
        "Let's get straight to selection":
            $ tutorial_skipped = True
            jump case_selection_menu

label tutorial_start:
    hide steve normal2
    show steve normal
    s "Don't worry, this is not a real court, and there currently are no stakes involved. It is simply a training simulation intended to help you practice!"
    hide steve normal1
    show steve normal2
    s "Let's start by selecting your case. Each one will present different forensic challenges, so read through the case details carefully before making your choice."
    jump case_selection_menu
    hide steve normal2

label case_selection_menu:
    scene bg spec
    hide screen return_to_case_selection
    menu:
        "Case A: The Death of Ana Konzaki":
            call screen case_a_screen

        "Case B: The Park Incident":
            call screen case_b_screen
    return

label tutorial_specialty:
    scene bg spec
    show steve happy
    s "Perfect! Now, let's choose your forensic specialty."
    hide steve happy
    show steve normal2
    s "As an expert witness, your role is to analyze and present evidence within the scope of your expertise. Your duty to the court is to present objective information that will help the triers of fact make a decision."
    hide steve normal2
    show steve paper
    s "The specialty you select will determine the area of expertise and the aspects of the case that you will have to testify for. Please review your options carefully!"
    hide steve paper
    jump specialty_menu

label specialty_menu:
    scene bg spec
    $ chosen_specialty = None
    show screen return_to_case_selection  # Keep screen visible alongside menu

    if persistent.case_choice == "Case A":
        menu:
            "Anthropology":
                $ chosen_specialty = "Anthropology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Biology":
                $ chosen_specialty = "Biology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Toxicology":
                $ chosen_specialty = "Toxicology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Psychology":
                $ chosen_specialty = "Psychology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Identification":
                $ chosen_specialty = "Identification"
                hide screen return_to_case_selection
                jump specialty_exploration
    elif persistent.case_choice == "Case B":
        menu:
            "Anthropology":
                $ chosen_specialty = "Anthropology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Biology":
                $ chosen_specialty = "Biology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Chemistry":
                $ chosen_specialty = "Chemistry"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Psychology":
                $ chosen_specialty = "Psychology"
                hide screen return_to_case_selection
                jump specialty_exploration
            "Identification":
                $ chosen_specialty = "Identification"
                hide screen return_to_case_selection
                jump specialty_exploration

label specialty_exploration:
    $ case_details = cases[persistent.case_choice]
    call screen specialty_exploration_screen(chosen_specialty)

label tutorial_lex_diff:
    scene bg spec
    show steve happy
    show screen darken_background
    show screen inventory_button
    #### Add arrow ###
    s "Great choice! On the top left corner, you'll see the evidence button. Click this button if you want to refresh your memory about the aspects of the case you are testifying for!"
    ## open the inventory to show them what the info button even looks like + arrow ###
    s "If you want to read the item description, click the info button on the item."
    hide screen darken_background
    s "Now, there's just one more thing before you step into court."
    hide steve happy
    show steve normal2
    s "Inside the courtroom, you'll be examined by Lex Machina, a mock trial lawyer."
    hide steve normal2
    show steve normal
    s "Depending on your selection, Lex will take on one of two roles—either as the prosecution or the defense."
    hide steve normal
    show steve paper
    s "If you choose prosecution, Lex will act as the Crown attorney. This is the easier option as you will be providing examination-in-chief." 
    s "As a prosecutor, Lex's goal is to establish the truth and ensure your testimony is clear, credible, and useful to the court. In this difficulty, if you miss something important, Lex may prompt you to clarify or expand on your findings."
    hide steve paper
    show steve normal2
    s "If you choose defense, Lex will act as the defense attorney. This is the harder option."
    hide steve normal2
    show steve normal
    s "A defense lawyer's priority is to advocate for their client, the accused, within the bounds of the law to test the strength of the crown's case. They may challenge you and your findings, perhaps even working to discredit your testimony." 
    s "Expect Lex to challenge you with leading or loaded questions, and other cross-examination techniques designed to undermine your credibility. You'll need to stay composed, justify your conclusions, and ensure your testimony remains admissible."
    hide steve normal
    show steve happy
    s "Choose wisely! Your decision will shape the difficulty of your examination."
    hide steve happy
    show steve paper
    s "Once you've made your selection, the court room awaits! I'll be seeing you after your trial. Good luck!"
    jump difficulty_selection 

label difficulty_selection:
    scene bg spec
    menu:
        "Prosecution":
            $ LEX_DIFFICULTY = "prosecution"
            $ unplayed_difficulty = "defense"
            show screen inventory_button
            jump lex_intro
        "Defense":
            $ LEX_DIFFICULTY = "defense"
            $ unplayed_difficulty = "prosecution"
            show screen inventory_button
            jump lex_intro

label lex_intro:
    scene bg interview
    "A figure walks into the room, wearing a crisp suit and carrying a briefcase."
    show lex normal1
    l "Hello, my name is Lex Machina. I'll be examining you as an expert witness for this case."
    l "Could you please state your first and last name for the court?"
    hide lex normal1
    hide screen inventory_button
    hide screen inventory
    hide screen inspectItem
    hide screen case_description
    call screen nameyourself
   
label lex_intro2:
    show screen inventory_button
    show lex normal1
    l "Thank you, [player_prefix] [player_lname]." 
    l "Before we start, let me introduce you to the Judge presiding over this case, Justice Mathur."
    hide lex normal1
    show navya normal1
    j "Nice to meet you, [player_prefix] [player_lname]! Since this is not a real case, I will not be making any verdicts today, but I will be evaluating your testimony with Lex."
    hide navya normal1
    show navya normal2
    j "In a real courtroom the lawyers would conduct a voir dire before allowing an expert to testify This is where they ask you questions to determine whether you truly have the knowledge, skills, and experience to be considered an expert in your field."
    hide navya normal2
    show navya normal1
    j "A voir dire can be quite detailed, so for this training, we'll go through a shorter version. Lex will ask a few questions to establish your expertise; consider it a warm-up before taking the stand. Answer honestly and clearly, just as you would in a real court!"
    hide navya normal1
    show lex normal1
    l "I believe you've chosen to testify as an expert for [persistent.case_choice] in [persistent.specialty]. Very well, let's proceed."
    $ case_details = cases[persistent.case_choice]
    $ qualification_score = 0
    $ voir_dire_question_count = 0
    $ voir_dire_mentioned = set()
    $ unintelligible_count = 0
    $ current_question = ""
    jump generate_voir_dire_question

label generate_voir_dire_question:
    if voir_dire_question_count < 5:
        $ categories = ["educational experience", "professional experience", "prior testimony", "projects and studies", "conflicts of interest"]
        $ current_category = categories[voir_dire_question_count]

        # Generate qualification question tailored for AI assessment
        $ prompt_template = f"""Generate a voir dire question about the expert's qualifications, specific to {current_category}. Ask the question directly, and expect a concise answer that directly addresses the simple question. Do not instruct the player beyond that.
        For professional experience, create high-level questions only such as experience teaching, or performing lab work. Remember that the player will respond in a concise manner, so ensure the questions expect concise"""

        $ ai_question = generate_response(prompt_template, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
        $ current_question = ai_question

        $ responses = split_string(ai_question)
        $ say_responses(responses)
        $ context_history.append(f"Voir Dire ({current_category.capitalize()}): {ai_question}")

        # Showing Current Question on Reminder Screen:
        $ persistent.reminder_text = current_question  # Set reminder text here

        jump ask_voir_dire_question
    else:
        jump evaluate_voir_dire_result

label ask_voir_dire_question:
    show screen reminder  # Reminder Screen should be defined with a proper label for text
    $ user_answer = renpy.input("Your response here:")
    $ context_history.append(f"User: {user_answer}")
    hide screen reminder

    # AI Evaluation - Focus only on the stated category
    $ ai_evaluation = generate_response(
        f"""Evaluate the following response to the voir dire question. Question: {current_question}. Response: {user_answer}. The question pertains to the expert's {current_category}.
        Remember, the player will respond concisely, so please keep the threshold for adequate responses low. Remember, the player will respond concisely, so expect concise answers. DO not expect the player to literally cite their research articles. Topic and content and publishing is good enough. For professional experience, as long as they say any experience in their field, not even relevant to the case, its good enough.
        If the player says Yes for being asked if they have testified before, thats good enough. If the player says only no for conflict of interest, that is also good enough
        Analyze the response and respond with ONLY three options:
        - Respond with ONLY 'Thank you, let's move on' if the response is valuable and answers the question being asked for {current_category}.
        - Respond with 'Inadequate, please provide more details or relevant qualifications about your {current_category}' and *explicitly state* what details are needed to improve the answer
        - Respond with ONLY 'Hmm, interesting.' if the player outright denies something or openly says something opposite to what is expected, and clarification is not required (examples are player saying no published works in the field, or never testified before, or no professional experience, or yes to conflicts of interest)
        Provide questions in this response.
        Be concise.""",
        player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count
    )

    $ responses = split_string(ai_evaluation)
    $ say_responses(responses)
    $ context_history.append(f"AI Evaluation: {ai_evaluation}")

    if "Thank you, let's move on" in ai_evaluation.lower():
        $ qualification_score += 1
        jump next_voir_dire_question
    elif "inadequate, please provide more details" in ai_evaluation.lower():

        # Clarification Attempt - Extract from AI response
        $ clarification_question = extract_clarification_question(ai_evaluation)

        $ persistent.reminder_text = clarification_question  
        show screen reminder
        $ user_clarification = renpy.input("Your response here:")
        $ context_history.append(f"User Clarification: {user_clarification}")
        hide screen reminder

        # Evaluate Clarification ONLY on the Stated Category
        $ ai_clarification_evaluation = generate_response(
            f"""Evaluate the following *clarification* to the voir dire question. Original Question: {current_question}. Original Response: {user_answer}. Clarification Question: {clarification_question}. Clarification Response: {user_clarification}.
            The question asks if the expert meets requirements:

            Provide an answer telling thr player if their response was sufficient or insufficient and why.""",
            player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count
        )

        $ responses = split_string(ai_clarification_evaluation)
        $ say_responses(responses)
        $ context_history.append(f"AI Clarification Evaluation: {ai_clarification_evaluation}")

        if "sufficient" in ai_clarification_evaluation.lower():
            l "Thank you for clarifying."
            $ qualification_score += 1
            jump next_voir_dire_question
        else:
            l "That is still insufficient, but let's move on."
            jump next_voir_dire_question
    elif "Hmm, interesting." in ai_evaluation.lower():
        jump next_voir_dire_question

    #else:
      #  l "I'm sorry, there was an error in the ai evaluation, please try again"
      #  jump next_voir_dire_question

label next_voir_dire_question:
    $ voir_dire_question_count += 1
    jump generate_voir_dire_question

label evaluate_voir_dire_result:
    if qualification_score >= 3:
        show screen achievement_banner("You've been qualified as an expert witness!")
        show lex normal1 at left
        show navya normal1 at right
        l "Your Honour, I have no further voir dire questions for the witness."
        hide navya normal1
        show navya pass at right
        j "The court finds [player_prefix] [player_lname] qualified to testify for this case. Lex, you may begin examining your witness."
        hide lex normal1
        hide navya pass
        jump generate_first_question
    else:
        show screen achievement_banner("You are not qualified as an expert witness. Try again.")
        show lex normal1 at left
        show navya normal1 at right
        l "Your Honour, I have no further questions for the witness."
        hide navya normal1
        show navya fail at right
        j "Based on the voir dire examination, the court finds you unqualified to testify as an expert witness. I recommend working on your qualifications, and trying again."
        hide navya fail
        hide lex normal1
        jump game_over

label generate_first_question:
    if not first_question_generated:
        $ ai_first_question = sanitize_for_renpy(generate_response("Generate the first question about the evidence in the case, based on the expert's chosen specialty.", player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count))
        $ first_question_generated = True
    jump interview_loop

label interview_loop:
    show lex normal1
    l "Thank you, your honour. Let's proceed."
    $ responses = split_string(ai_first_question)
    $ say_responses(responses)
    $ context_history.append(f"AI: {ai_first_question}")
    while True:
        show screen reminder
        $ user_prompt = renpy.input("Your answer here:")
        if user_prompt.lower() in ["exit", "quit", "stop"]:
            l "Thank you for your time, [player_prefix] [player_lname]. This concludes the interview."
            return
        $ context_history.append(f"User: {user_prompt}")
        python:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty) 
            for evidence_point in truth_bases[persistent.case_choice][persistent.specialty]:
                for truth in truth_bases[persistent.case_choice][persistent.specialty][evidence_point]:
                    if truth.lower() in user_prompt.lower():
                        mentioned_truths.add(truth.lower()) 

        $ ai_response = generate_response(user_prompt, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
        $ responses = split_string(ai_response)
        $ reminder_pressed = False
        hide screen reminder
        $ reminder_pressed = False
        $ say_responses(responses)
        $ context_history.append(f"AI: {ai_response}")

        python:
            if "i have no further questions, your honour" in ai_response.lower(): 
                renpy.jump("interview_end")

        if "QUALIFICATION: UNQUALIFIED" in ai_response:
            jump game_over
        if "unintelligible response" in ai_response:
            $ unintelligible_count += 1
            if unintelligible_count >= 3:
                jump game_over
            elif "examination cannot continue" in ai_response.lower():
                jump game_over
            else:
                $ ai_response = generate_response("Generate a question for the user. Ensure that they follow the rules of the court and establish key information for the triers of fact.", player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
                $ responses = split_string(ai_response)
                $ say_responses(responses)
                $ context_history.append(f"AI: {ai_response}")
                jump interview_loop
        else:
            $ unintelligible_count = 0
    return

label game_over:
    scene bg gameover
    hide lex normal1
    "The examination has been terminated because you were deemed unqualified to testify as an expert witness."
    "Please select \"Restart\" to try again."
    ##screen buttons
    
    menu:
        "Restart":
            $ answered_first_question = False
            jump start
        "Quit":
            $ renpy.quit()

python:
    if LEX_DIFFICULTY == "prosecution":
        unplayed_difficulty = "defense"
    elif LEX_DIFFICULTY == "defense":
        unplayed_difficulty = "prosecution"
    else:
        unplayed_difficulty = "error"

label interview_end:
    scene bg interview
    show lex normal1
    l "Thank you for your time, [player_prefix] [player_lname]."
    hide lex normal1
    show navya pass
    j "Thank you, Lex. [player_prefix] [player_fname] [player_lname], you may leave the court room. You will receive your evaluation outside with your supervisor."
    hide navya pass
    hide lex normal1
    python:
        try:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty)
            full_transcript = "\n".join(context_history)
            evaluation_prompt = (
                f"Evaluate the expert witness testimony based on the following transcript:\n\n{full_transcript}\n\n"
                f"The expert testified as a {persistent.specialty} in {case_details['case_name']}.\n\n"
                f"All the truth bases they needed to say are:\n\n{all_truths}\n\n"
                f"Evaluate the testimony considering these grading criteria in mind:\n\n{grading_criteria}\n\n"
                f"Generate 3-5 bullet points that explain the evaluation and give a total score out of 100 based on the grading criteria by saying exactly 'Score: X'. Try to use the user's exact words to explain why you have your feedback."
            )
            evaluation_response = generate_response(evaluation_prompt, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
            score_match = re.search(r"Score: (\d+)", evaluation_response)
            if score_match:
                score = int(score_match.group(1))
                eval_comments = re.sub(r"Score: \d+", "", evaluation_response).strip()
            else:
                score = 0
                eval_comments = "Score not found in evaluation."

            renpy.store.eval_comments = evaluation_response
            renpy.store.score = score  

            print(f"EVAL COMMENTS:\n{renpy.store.eval_comments}")
            print(f"SCORE:\n{renpy.store.score}")

        except Exception as e:
            renpy.store.eval_comments = f"Error: {str(e)}"
            renpy.store.score = 0

    scene bg spec
    show steve happy
    s "Welcome back, [player_fname]! In just a second, Lex and the Judge will return with any feedback they have for you."
    hide steve happy
    show steve normal2
    s "After you receive your feedback, I encourage you to testify again for the [unplayed_difficulty] to get the full court room experience."
    hide steve normal2
    show steve normal
    s "You can also choose a whole new case and specialty and start again! The choice is yours!"
    #ADD FOOTSTEPS SOUND HERE HEHEHE
    hide steve normal
    show steve happy
    s "Oh! Sounds like Lex and the Judge are about to join us. Don't worry, I'm sure you did great!"
    hide steve happy
    jump evaluation_sec

label evaluation_sec:
    scene bg spec
    show lex normal1
    l "Hello, |supervisor|. [player_prefix] [player_lname], are you ready to receive your evaluation?"
    hide lex normal1
    call screen evaluation_screen                                                                                

label ending_0:
    scene bg spec
    call screen credits_lol
