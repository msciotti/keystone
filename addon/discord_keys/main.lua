local DiscordKeys = CreateFrame("Frame");
DiscordKeys:RegisterEvent("ADDON_LOADED");
DiscordKeys:RegisterEvent("PLAYER_ENTERING_WORLD");

DiscordKeys:SetScript("OnEvent", function(self, event, arg1)
    if event == "ADDON_LOADED" and arg1 == "CurrentKey" then
        CurrentKey = nil

    elseif event == "PLAYER_ENTERING_WORLD" then
        for container=0, 4, 1 do
            local num_slots = GetContainerNumSlots(container);
            for slot=num_slots, 0, -1 do
                local _, _, _, _, _, _, slotLink, _, _, slotItemId = GetContainerItemInfo(container,slot);
                if slotLink and slotLink:match("Keystone:") then
                    local item = GetContainerItemLink(container, slot);
                    print(item)
                    CurrentKey = item;
                end
            end
        end
    end
end)
