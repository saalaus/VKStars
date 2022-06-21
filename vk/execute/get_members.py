"""Get 25 000 members on one execute
Params: group_id, offset"""
code = """
var group_id = %(group_id)d;
var i = 0;
var offset = %(offset)d;
var members = [];
var all_count = 0;
while (i < 25){
    i = i+1;
    var api = API.groups.getMembers({"group_id": group_id, "offset": offset, "count":1000});
    if (api.items){
        members = members + api.items;
        offset = offset + 1000;}
        all_count = api.count;
    }
var end = false;
if (offset >= all_count){
    end = true;
}
return {"count": members.length, "all_count": all_count, "end": end, "items": members};
"""
