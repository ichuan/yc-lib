#import <Foundation/Foundation.h>

#define bool BOOL

static int counter = 0;
@interface Test: NSObject {
@public
    int x;
}
//@property int x;
+(int) getCounter;
@end

@implementation Test
//@synthesize x;
+(int) getCounter{
    return counter++;
}
@end

int main (int argc, const char * argv[])
{
        NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
        Test *t = [[Test alloc] init];
        int i = 0;
        for (; i < 10; i++)
            NSLog(@"%i", [Test getCounter]);
        t->x = 110;
        NSLog(@"%i", t->x);

        [pool drain];
        return 0;
}
