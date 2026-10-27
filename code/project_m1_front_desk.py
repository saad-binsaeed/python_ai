BOT_NAME = "Sweet Treats Assistant"
DELIVERY_FEE = 250.0
FREE_DELIVERY_LIMIT = 2000.0
CLOUD_PRICE_PER_1K_TOKENS = 0.5

message_count = 0
rules_answered_count = 0
unanswered_count = 0
quote_count = 0
total_quoted_value = 0.0
total_ai_cost = 0.0

# header with separators and asking customer name once before the loop 
print("=" * 60)
print(f"--- Welcome to {BOT_NAME} ---")
print("=" * 60)

raw_name = input("Please enter your name: ")
customer_name = raw_name.strip().title()

print(f"\nHello {customer_name}! How can we make your day sweeter? (Type 'bye' to exit, or '/quote' for orders)\n")

# Main conversation loop using while True (Requirement 8)
while True:
    raw_msg = input(f"{customer_name}: ")
    
    msg = raw_msg.strip().lower()

    if msg == "":
        continue

    if msg in ["bye", "goodbye", "exit"]:
        print(f"\n{BOT_NAME}: Goodbye {customer_name}! Have a wonderful day.")
        break
        
    message_count += 1
    
    # complaint rule first so unhappy customers reach a human immediately (Requirement 6)
    if any(word in msg for word in ["complaint", "refund", "late", "bad", "issue"]):
        rules_answered_count += 1
        print(f"{BOT_NAME}: We are very sorry to hear about your experience, {customer_name}. Our store manager has been alerted and will contact you immediately.")
        
    # greetings checked with == or .startswith(), not in (Requirement 7)
    elif msg == "hi" or msg == "hello" or msg.startswith("hey"):
        rules_answered_count += 1
        print(f"{BOT_NAME}: Hello {customer_name}! Welcome back to Sweet Treats Bakery.")
        
    # hours intent
    elif "hours" in msg or "timings" in msg or "open" in msg:
        rules_answered_count += 1
        print(f"{BOT_NAME}: We are open daily from 9:00 AM to 10:00 PM.")
        
    # Location intent
    elif "location" in msg or "address" in msg or "where" in msg:
        rules_answered_count += 1
        print(f"{BOT_NAME}: We are located at Main Commercial Boulevard, Block Y.")
        
    # Delivery info intent
    elif "delivery" in msg:
        rules_answered_count += 1
        print(f"{BOT_NAME}: Delivery fee is {DELIVERY_FEE:,.2f} PKR, but it's FREE for orders above {FREE_DELIVERY_LIMIT:,.2f} PKR!")
        
    #  General Menu info intent
    elif "menu" in msg or "items" in msg:
        rules_answered_count += 1
        print(f"{BOT_NAME}: We offer Brownies (300 PKR), Croissants (250 PKR), and Birthday Cakes (1,500 PKR). Type '/quote' to calculate an order price!")
        
   #quote price calculator (Requirements 9, 10, 11, 12)
    elif msg.startswith("/quote"):
        rules_answered_count += 1
        quote_count += 1
        
        print(f"{BOT_NAME}: Let's build your custom quote.")
        item_input = input(f"{BOT_NAME}: Choose an item (Brownies / Croissant / Cake): ").strip().lower()
        
        try:
            quantity = int(input(f"{BOT_NAME}: Enter quantity: "))
        except ValueError:
            print(f"{BOT_NAME}: Invalid quantity entered. Quote cancelled.")
            continue
            
        # Item pricing with if / elif / else
        if "brownie" in item_input:
            unit_price = 300.0
            item_name = "Brownies"
        elif "croissant" in item_input:
            unit_price = 250.0
            item_name = "Croissants"
        elif "cake" in item_input:
            unit_price = 1500.0
            item_name = "Birthday Cakes"
        else:
            print(f"{BOT_NAME}: '{item_input}' is not on our menu.")
            continue
            
        subtotal = unit_price * quantity
        
        # Why: We apply a bulk discount rule (10% off for 10 or more items) to incentivize larger customer orders.
        if quantity >= 10:
            discount = subtotal * 0.10
        else:
            discount = 0.0
            
        discounted_subtotal = subtotal - discount
        
        # Why: Free delivery applies if the discounted order meets or exceeds the minimum threshold.
        if discounted_subtotal >= FREE_DELIVERY_LIMIT:
            delivery_cost = 0.0
        else:
            delivery_cost = DELIVERY_FEE
            
        total = discounted_subtotal + delivery_cost
        total_quoted_value += total
        
        # Print with thousand separators (:,)
        print(f"\n--- Price Quote Summary ---")
        print(f"Item: {item_name} x {quantity}")
        print(f"Subtotal: {subtotal:,.2f} PKR")
        print(f"Discount: {discount:,.2f} PKR")
        print(f"Delivery: {delivery_cost:,.2f} PKR")
        print(f"Total Amount: {total:,.2f} PKR\n")
        
    #smart fallback for anything rules cannot answer (Requirements 13, 14, 15, 16)
    else:
        unanswered_count += 1
        
        clean_question = raw_msg.strip().capitalize()[:150]
        
        estimated_tokens = round(len(clean_question) / 4)
        
        if any(private_word in msg for private_word in ["phone", "cnic", "address", "credit card", "password", "secret"]):
            chosen_model = "Local Model (Ollama - Privacy Secure)"
            ai_cost = 0.0
        else:
            chosen_model = "Cheap Cloud Model (Gemini-Flash)"
            ai_cost = (estimated_tokens / 1000) * CLOUD_PRICE_PER_1K_TOKENS
            
        total_ai_cost += ai_cost
        
        print(f"{BOT_NAME} [Smart Fallback Routing]:")
        print(f"Chosen Model: {chosen_model}")
        
        ai_prompt = f"""
        --- AI Prompt ---
        Customer: {customer_name}
        Query: {clean_question}
        Instruction: Answer concisely as Sweet Treats Bakery customer support.
        -----------------
        """
        print(ai_prompt)
print("$",50)
print(f"--- Session Report for {customer_name} ---")
print(f"Total messages sent: {message_count}")
print(f"Answered by rules: {rules_answered_count}")
print(f"Unanswered (fallback): {unanswered_count}")
print(f"Number of quotes generated: {quote_count}")
print(f"Total quoted value: {total_quoted_value:,.2f} PKR")
print(f"Total estimated AI cost: {total_ai_cost:.4f} PKR")
print("$",50)
