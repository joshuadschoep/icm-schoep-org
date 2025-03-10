import { Button } from "@/components/ui/button";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { XIcon } from "lucide-react";
import { useCallback } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";

const ActivePlayerLabel = "+ Add Player";
const DisabledPlayerLabel = "! Maximum Reached";

/**
 * Requires react-hook-form provider
 */
export const PlayersForm = () => {
  const { control } = useFormContext();

  const { fields, append, remove } = useFieldArray({
    control,
    name: "players",
  });

  const addNewPlayer = useCallback(() => {
    append({ stack: "", name: undefined });
  }, [append]);

  return (
    <fieldset className="grid gap-3 content-start py-6">
      <legend className="my-3 md:mt-6 m-auto">Remaining Players</legend>
      {fields.map((field, index) => (
        <div key={field.id} className="grid grid-cols-[1fr_1fr_auto] gap-3">
          <FormField
            control={control}
            name={`players.${index}.stack`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Player {index + 1} stack</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name={`players.${index}.name`}
            render={({ field }) => (
              <FormItem>
                <FormLabel className="flex flex-row">
                  Player {index + 1} name (optional)
                </FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button
            className="self-end text-red-600 border-red-600 cursor-pointer hover:bg-red-50 hover:text-red-700 hover:border-red-700"
            onClick={() => remove(index)}
            type="button"
            variant="outline"
            size="icon"
          >
            <XIcon />
          </Button>
        </div>
      ))}
      <Button
        className="cursor-pointer"
        type="button"
        onClick={addNewPlayer}
        disabled={fields.length >= 10}
      >
        {fields.length < 10 ? ActivePlayerLabel : DisabledPlayerLabel}
      </Button>
    </fieldset>
  );
};
