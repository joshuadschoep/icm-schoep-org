import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import "./header.css";

export const Header = () => {
  return (
    <header className="p-5 bg-white shadow-lg">
      <div className="max-w-5xl m-auto flex flex-col items-center md:flex-row gap-5 align-center justify-between">
        <hgroup>
          <h1 className="text-xl">Independent Chip Model</h1>
          <h2 className="text-lg font-semibold">Calculator</h2>
        </hgroup>
        {/* <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink
                href="/"
                className={navigationMenuTriggerStyle()}
              >
                Tool
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink
                href="/philosophy"
                className={navigationMenuTriggerStyle()}
              >
                Philosophies
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink
                href="/validation"
                className={navigationMenuTriggerStyle()}
              >
                Validation
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu> */}
      </div>
    </header>
  );
};
