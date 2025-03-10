import { Button } from "@/components/ui/button";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { getOrdinal } from "@/lib/utils";
import { XIcon } from "lucide-react";
import { useFormContext } from "react-hook-form";

const ActivePayoutLabel = "+ Add Payout";
const DisabledPayoutLabel = "! Maximum Reached";

export const PayoutsForm = () => {
  const { control, watch, setValue } = useFormContext();
  const payouts = watch("payouts") as number[];

  return (
    <fieldset className="grid gap-3 content-start py-6">
      <legend className="my-3 md:mt-6 m-auto">Payouts</legend>
      {payouts.map((value, index) => (
        <div key={index} className="grid grid-cols-[1fr_auto] gap-3">
          <FormField
            control={control}
            name={`payouts.${index}`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>{getOrdinal(index + 1)} place</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button
            className="self-end text-red-600 border-red-600 cursor-pointer hover:bg-red-50 hover:text-red-700 hover:border-red-700"
            onClick={() => {
              payouts.splice(index, 1);
              setValue("payouts", payouts);
            }}
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
        onClick={() => {
          payouts.push(0);
          setValue("payouts", payouts);
        }}
        disabled={payouts.length >= 10}
      >
        {payouts.length < 10 ? ActivePayoutLabel : DisabledPayoutLabel}
      </Button>
    </fieldset>
  );
};
