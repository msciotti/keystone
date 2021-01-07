local DiscordKeys = CreateFrame("Frame");
DiscordKeys:RegisterEvent("PLAYER_ENTERING_WORLD");

function DiscordKeys:OnEvent(event, arg1)
    if event == "PLAYER_ENTERING_WORLD" then
        for container=0, 4, 1 do
            local num_slots = GetContainerNumSlots(container);
            for slot=num_slots, 0, -1 do
                local _, _, _, _, _, _, slotLink, _, _, slotItemId = GetContainerItemInfo(container,slot);
                if slotLink and slotLink:match("Keystone:") then
                    local item = GetContainerItemLink(container, slot);
                    CurrentKey = item;
                end
            end
        end
    end
end
