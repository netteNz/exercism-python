import json

class RestAPI:
    def __init__(self, database=None):
        self.database = {"users": []} if database is None else database

    def get(self, url, payload=None):
        if url == "/users":
            if payload is None:
                # Return all users
                return {"users": self.database["users"]}
            else:
                # Parse the payload
                try:
                    data = json.loads(payload) if isinstance(payload, str) else payload
                    requested_users = data.get("users", [])
                    
                    # Filter users and sort by name
                    filtered_users = [user for user in self.database["users"] 
                                     if user["name"] in requested_users]
                    sorted_users = sorted(filtered_users, key=lambda x: x["name"])
                    
                    return {"users": sorted_users}
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Error parsing payload: {e}")
                    return {"error": "Invalid payload"}
        
        # Handle other endpoints or return error
        return {"error": "Endpoint not found"}

    def post(self, url, payload):
        try:
            data = json.loads(payload) if isinstance(payload, str) else payload
            
            if url == "/add":
                # Create a new user
                new_user = {
                    "name": data["user"],
                    "owes": {},
                    "owed_by": {},
                    "balance": 0.0
                }
                
                # Add to database
                self.database["users"].append(new_user)
                return new_user
                
            elif url == "/iou":
                # Handle IOU creation
                lender_name = data["lender"]
                borrower_name = data["borrower"]
                amount = float(data["amount"])
                
                # Find the users
                lender = None
                borrower = None
                
                for user in self.database["users"]:
                    if user["name"] == lender_name:
                        lender = user
                    if user["name"] == borrower_name:
                        borrower = user
                
                # Update lender's records
                if borrower_name in lender["owes"]:
                    # If lender already owes borrower
                    if lender["owes"][borrower_name] >= amount:
                        lender["owes"][borrower_name] -= amount
                        if lender["owes"][borrower_name] == 0:
                            del lender["owes"][borrower_name]
                    else:
                        remaining = amount - lender["owes"][borrower_name]
                        del lender["owes"][borrower_name]
                        lender["owed_by"][borrower_name] = lender["owed_by"].get(borrower_name, 0) + remaining
                else:
                    # Simple case: borrower owes lender more
                    lender["owed_by"][borrower_name] = lender["owed_by"].get(borrower_name, 0) + amount
                
                # Update borrower's records
                if lender_name in borrower["owed_by"]:
                    # If borrower already is owed by lender
                    if borrower["owed_by"][lender_name] >= amount:
                        borrower["owed_by"][lender_name] -= amount
                        if borrower["owed_by"][lender_name] == 0:
                            del borrower["owed_by"][lender_name]
                    else:
                        remaining = amount - borrower["owed_by"][lender_name]
                        del borrower["owed_by"][lender_name]
                        borrower["owes"][lender_name] = borrower["owes"].get(lender_name, 0) + remaining
                else:
                    # Simple case: borrower owes lender more
                    borrower["owes"][lender_name] = borrower["owes"].get(lender_name, 0) + amount
                
                # Recalculate balances
                total_owed_by_others_lender = sum(lender["owed_by"].values())
                total_owed_to_others_lender = sum(lender["owes"].values())
                lender["balance"] = total_owed_by_others_lender - total_owed_to_others_lender
                
                total_owed_by_others_borrower = sum(borrower["owed_by"].values())
                total_owed_to_others_borrower = sum(borrower["owes"].values())
                borrower["balance"] = total_owed_by_others_borrower - total_owed_to_others_borrower
                
                # Return updated users
                updated_users = [lender, borrower]
                return {"users": sorted(updated_users, key=lambda x: x["name"])}
            
            return {"error": "Invalid endpoint"}
            
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error in POST: {e}")
            return {"error": "Invalid payload"}

